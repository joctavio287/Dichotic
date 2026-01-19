"""
This script preprocesses raw EEG data files in BDF format. The preprocessing steps include:
- Loading and renaming channels to standard 10-20 system names.
- Dropping unused external channels and setting channel types.
- Applying filters (high-pass, low-pass, and notch).
- Annotating non-listening periods as 'bad'.
- Downsampling the data to a target sampling rate.
- Rereferencing to mastoids.
- Performing ICA to remove artifacts, with visualizations saved for inspection.
- Saving the preprocessed data and event times.
"""
# 1. TODO usar el mismo nombre para psychopy y biosemi--> sugerir sin guión bajo --> DICHOTIC001
# 2. TODO mne.find_events no funciona bien porque no se escribieron bien los triggers
# 3. TODO: no aparecen las marcas del offset 105
# 4. TODO: se generan marcas no esperadas 
# 5. TODO: hubo que hacer hacks porque aparecieron marcas esperadas, pero en momentos extraños
# 6. TODO: aplicar filtros reproducibles -> revisar repo speech-encoding

import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm
import numpy as np
import mne

from utils.processing import (
    find_first_event_on_id,
    dump_dict_to_json,
    load_json_to_dict,
    get_no_task_times
)
import config

PREPROCESSED_DIR_TRIGGERS = config.PREPROCESSED_DIR / "triggers"
PREPROCESSED_DIR_ANNOT = config.PREPROCESSED_DIR / "annotations"
PREPROCESSED_DIR_FIF = config.PREPROCESSED_DIR / "fif"
FIGURES_ICA = config.FIGURES_DIR / "ICA"

PREPROCESSED_DIR_TRIGGERS.mkdir(parents=True, exist_ok=True)
PREPROCESSED_DIR_ANNOT.mkdir(parents=True, exist_ok=True)
PREPROCESSED_DIR_FIF.mkdir(parents=True, exist_ok=True)
FIGURES_ICA.mkdir(parents=True, exist_ok=True)

mne.set_log_level(config.VERBOSE_LEVEL)

for eeg_path in tqdm(list(config.EEG_DIR.glob("*.bdf")), desc="Preprocessing EEG files"):
    
    # Load behavioural and psychopy data if needed
    behavioural_data = load_json_to_dict(
        config.BEHAVIOURAL_DIR / f"{eeg_path.stem.split('prueba')[1]}_behavioural.json" # FIXME 1
    )

    # Load raw EEG data
    raw = mne.io.read_raw_bdf(
        eeg_path, preload=True, verbose=config.VERBOSE_LEVEL
    )

    # =================
    # Events extraction

    # Define events and epochs prior to downsampling and rereferencing 
    trigger = raw.get_data()[-1, :]
    unique_trigger_values = np.unique(trigger[trigger != 0])
    
    # Listening events
    listening_onsets = find_first_event_on_id(
        event_id=config.TRIGGER_IDS['listening'][0],
        trigger_signal=trigger,
        raw=raw
    )
    # FIXME 3
    # listening_offsets = find_first_event_on_id(
    #     event_id=config.TRIGGER_IDS['listening'][1],
    #     trigger_signal=trigger,
    #     raw=raw
    # )
    # np.unique(
    #     trigger[trigger == config.TRIGGER_IDS['listening'][0]], 
    #     return_counts=True
    # )
    # np.unique(
    #     trigger[trigger == config.TRIGGER_IDS['listening'][1]], 
    #     return_counts=True
    # )
    # listening_durations = listening_offsets - listening_onsets
    listening_durations = np.array(
        behavioural_data['listening_presentation']['audiobook_duration']
    )
    listening_offsets = listening_onsets + listening_durations
    
    # Get non-listening periods
    no_task_onsets, no_task_durations = get_no_task_times(
        offsets=listening_offsets,
        onsets=listening_onsets,
        raw=raw
    )
    
    # Annotate non-listening periods: will be rejected for ICA
    annotations = mne.Annotations(
        onset=no_task_onsets, 
        duration=no_task_durations, 
        description=['bad'] * len(no_task_onsets) 
    )
    raw = raw.set_annotations(
        annotations,
        verbose=config.VERBOSE_LEVEL
    )
    
    # Now find bips
    all_bips_onsets = []
    all_bips_durations = []
    all_bips_descriptions = []

    for bip_block in ['bips1', 'bips2']:
        for bip_number in range(config.TRIGGER_IDS[bip_block][2]):

            # Calculate trigger value for current bip
            trigger_value = config.TRIGGER_IDS[bip_block][0] + bip_number * config.TRIGGER_IDS[bip_block][1]
            
            bips_onsets = find_first_event_on_id(
                event_id=trigger_value,
                trigger_signal=trigger,
                raw=raw
            )
            bips_offsets = find_first_event_on_id(
                event_id=trigger_value+1,
                trigger_signal=trigger,
                raw=raw
            )
            # FIXME 4
            # Discard bips that don't have both onset and offset
            if (trigger_value not in unique_trigger_values):
                continue
            else:
                if len(bips_onsets) != len(bips_offsets):
                    bip_durations = np.array([1] * len(bips_onsets))
                    if len(bips_onsets) == 6:
                        # FIXME 5 hack to avoid a weird extra bip at start of block in bip 6 of first block
                        bips_onsets=bips_onsets[1:] 
                    elif len(bips_onsets) == 8:
                        # FIXME 5 hack to avoid a weird extra bip at start of block in bip 7 of second block
                        bips_onsets=bips_onsets[[0, 2, 3, 4 ,6]]
                else:
                    bip_durations = bips_offsets - bips_onsets
            all_bips_onsets.extend(bips_onsets.tolist())
            all_bips_durations.extend(bip_durations.tolist())
            all_bips_descriptions.extend(
                [f'bip_Block_{bip_block[-1]}_Bip_{bip_number+1}'] * len(bips_onsets) 
            )

    # Sort all bip annotations by onset time (since we processed blocks separately)
    sorted_indices = np.argsort(all_bips_onsets)
    all_bips_onsets = [all_bips_onsets[i] for i in sorted_indices]
    all_bips_durations = [all_bips_durations[i] for i in sorted_indices]
    all_bips_descriptions = [all_bips_descriptions[i] for i in sorted_indices]

    # ======================
    # Preprocessing eeg data 

    # Rename channels to standard 10-20 names
    raw = raw.rename_channels(config.EXTERNAL_MAPPING, verbose=config.VERBOSE_LEVEL)
    raw = raw.rename_channels(config.BIOSEMI_MAPPING, verbose=config.VERBOSE_LEVEL)
    
    # Drop unused external channels, set channel types and montage
    raw = raw.drop_channels(config.UNUSED_EXT_CH)  
    raw = raw.set_channel_types(config.CH_TYPES, verbose=config.VERBOSE_LEVEL)

    biosemi_montage = mne.channels.make_standard_montage('biosemi64')
    std_1020 = mne.channels.make_standard_montage('standard_1020')

    # Assign channel position to mastoids from standard 10-20 montage
    ch_pos = biosemi_montage.get_positions()['ch_pos']
    std_1020_pos = std_1020.get_positions()['ch_pos']
    ch_pos['M1'] = std_1020_pos['TP9']
    ch_pos['M2'] = std_1020_pos['TP10']
    combined_montage = mne.channels.make_dig_montage(
        ch_pos=ch_pos, 
        coord_frame='head'
    )
    raw = raw.set_montage(
        combined_montage, 
        on_missing='ignore' # dont assign positions to external channels
    )

    # Filter data: high pass 1 Hz Butterworth; Low pass 40 Hz; Notch 50 Hz. All non-causal # FIXME 6
    raw = raw.filter(
        l_freq=1, 
        h_freq=40,
        method='fir',
        phase='zero', 
        fir_design='firwin',
        verbose=config.VERBOSE_LEVEL
    )
    raw = raw.notch_filter(
        freqs=50,
        method='fir',
        phase='zero',
        fir_design='firwin',
        verbose=config.VERBOSE_LEVEL
    )
    
    # Downsample 
    raw = raw.resample(config.TARGET_SAMPLING_RATE, verbose=config.VERBOSE_LEVEL)

    # Rereference to mastoids
    raw = raw.set_eeg_reference(
        ['M1', 'M2'],
        verbose=config.VERBOSE_LEVEL
    )
    
    # ICA to remove artifacts
    ica = mne.preprocessing.ICA(
        n_components=config.ICA_PERCENTAGE, 
        method="infomax", 
        random_state=config.RANDOM_SEED,
        fit_params={'extended': True}, # to better separate sources. The extended version of the Infomax algorithm is designed to handle sub-Gaussian sources more effectively (line source for e.g).
    )
    ica = ica.fit(
        raw, 
        picks='eeg', 
        reject_by_annotation=True, # reject 'bad' annotations
        verbose=config.VERBOSE_LEVEL
    ) 

    # Plot ICA components for inspection
    sub_fig_path = FIGURES_ICA / f'{eeg_path.stem}'
    sub_fig_path.mkdir(parents=True, exist_ok=True)
    for component in np.arange(ica.n_components_):
        plt.close('all')
        fig = ica.plot_properties(
            raw, 
            picks=[component], 
            show=False, 
            verbose='CRITICAL'
        ) 
        fig[0].savefig(
            sub_fig_path / f"{component}_properties.png"
        )
    plt.close('all')
    fig = ica.plot_components(show=False)
    if ica.n_components_ >= 20:
        fig1, fig2 = fig
        fig1.savefig(sub_fig_path / "topo1.png")
        fig2.savefig(sub_fig_path / "topo2.png")
    else:
        fig.savefig(sub_fig_path / "topo.png")
    plt.close('all')
    fig = ica.plot_sources(raw, show=False)
    fig.savefig(sub_fig_path / "sources.png")
    
    # Remove artifact components based on predefined list
    ica.exclude = config.ICA_REMOVAL[eeg_path.stem] if eeg_path.stem in config.ICA_REMOVAL.keys() else []
    raw = ica.apply(raw)

    # Erase 'bad' annotations to avoid issues later on
    raw.set_annotations(None)
    
    # Save preprocessed data
    raw.save(
        PREPROCESSED_DIR_FIF / f"{eeg_path.stem}_preprocessed.fif", 
        verbose=config.VERBOSE_LEVEL,
        overwrite=True,
    )

    # Save events times to json
    events_times = {
        'listening_onsets': listening_onsets,
        'listening_durations': listening_durations,
        'listening_annotations': ['listening'] * len(listening_onsets),
        'no_task_durations': no_task_durations,
        'no_task_onsets': no_task_onsets,
        'no_task_annotations': ['no-task'] * len(no_task_onsets),
        'bips_onsets': all_bips_onsets,
        'bips_durations': all_bips_durations,
        'bips_descriptions': all_bips_descriptions
    }
    dump_dict_to_json(
        filepath=PREPROCESSED_DIR_ANNOT / f"events_{eeg_path.stem}.json",
        data_dict=events_times
    )
   
    # Save the last channel (triggers) separately
    np.save(
        PREPROCESSED_DIR_TRIGGERS / f"events_{eeg_path.stem}.npy", trigger
    )