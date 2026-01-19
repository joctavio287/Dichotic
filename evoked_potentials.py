from pathlib import Path
import pandas as pd
import numpy as np
import mne

from utils.processing import load_json_to_dict
from utils.figures_helpers import (
    onsets_plot, evoked_potential_plot
)
import config

OUTPUT_FIGURES_DIR = config.FIGURES_DIR / "evoked_potentials"
ANNOT_DIR = config.PREPROCESSED_DIR / 'annotations'
TRIGGER_DIR = config.PREPROCESSED_DIR / 'triggers'
FIF_DIR = config.PREPROCESSED_DIR / 'fif'

TMING_WINDOW = (-.2, .8)  # Time window around the bip stimuli in seconds
BASELINE = None  # No baseline correction

ID_NAMES = {
    'listening_bip_nontarget': 3,
    'listening_bip_target': 2,
    'bip': 1
}
labels_map = {
    1: 'Silence Bip',
    2: 'Listening Bip Target',
    3: 'Listening Bip Non-Target'
}
for eeg_file in FIF_DIR.glob("*_preprocessed.fif"):
    eeg_name = eeg_file.stem.replace(
         "_preprocessed", ""
    )
    output_figdir = OUTPUT_FIGURES_DIR / f"{eeg_name}"
    output_figdir.mkdir(parents=True, exist_ok=True)

    # Load behavioural data 
    behavioural_data = load_json_to_dict( #FIXME: usar la misma convención de nombres para psychopy y biosemi
        config.BEHAVIOURAL_DIR / f"{eeg_name.split('prueba')[1]}_behavioural.json"
    )
    subject_audiofile_codes = behavioural_data['metadata']['audio_filecodes']
    # subject_targets = behavioural_data['metadata']['target'] #TODO: arreglar esto
    subject_targets = [
        "R",
        "R",
        "R",
        "R",
        "R"
    ]

    # Read preprocessed EEG data
    raw = mne.io.read_raw_fif(eeg_file, preload=True, verbose=config.VERBOSE_LEVEL)
    raw = raw.pick_types(eeg=True, exclude=['M1', 'M2'])
    info_mne = raw.info.copy()

    # Read json annotation file
    annotations_data = load_json_to_dict(
        filepath=ANNOT_DIR / f"events_{eeg_name}.json"
    )
    
    # Create epochs around bip stimuli
    bips_indexes = raw.time_as_index(
        annotations_data['bips_onsets']
    )
    bip_events = np.zeros(
        shape=(len(bips_indexes), 3), dtype=int
    ) 
    bip_events[:,0] = bips_indexes
    bip_events[:,2] = ID_NAMES['bip']

    # Create epochs to audiobook listening periods
    listening_onsets = annotations_data['listening_onsets']
    listening_onsets_non_target = []
    listening_onsets_target = []
    for subject_audiofile_code, listening_onset, target in zip(
        subject_audiofile_codes,
        listening_onsets,
        subject_targets
    ):
        onsets_df = pd.read_csv(config.ONSETS_DIR / f"{subject_audiofile_code}_onsets.csv")
        for onset in onsets_df.values:
            listening_onsets_target.append(listening_onset + onset[0 if target=='L' else 1])
            listening_onsets_non_target.append(listening_onset + onset[1 if target=='L' else 0])
    
    listening_indexes_target = raw.time_as_index(listening_onsets_target)
    listening_events_target = np.zeros(
        shape=(len(listening_indexes_target), 3), dtype=int
    ) 
    listening_events_target[:,0] = listening_indexes_target
    listening_events_target[:,2] = ID_NAMES['listening_bip_target']
    listening_indexes_nontarget = raw.time_as_index(listening_onsets_non_target)
    listening_events_nontarget = np.zeros(
        shape=(len(listening_indexes_nontarget), 3), dtype=int
    )
    listening_events_nontarget[:,0] = listening_indexes_nontarget
    listening_events_nontarget[:,2] = ID_NAMES['listening_bip_nontarget']
    
    # Combine all events into a single array for epoching
    all_events = np.vstack((
        bip_events,
        listening_events_target,
        listening_events_nontarget
    ))
    all_events = all_events[
        np.argsort(all_events[:,0]) # sort events by time
    ]  
    
    # Plot event onsets
    onsets_plot(
        output_filepath=output_figdir / f"evoked_potential_onsets.png",
        events_times=[raw.times[bip_events[:,0]], raw.times[listening_events_target[:,0]], raw.times[listening_events_nontarget[:,0]]],
        events_labels=['Bip Events', 'Listening Target Events', 'Listening Non-Target Events'],
        events=[bip_events, listening_events_target, listening_events_nontarget],
        xlim=(0, 60*2), # First 2 minutes
        show=False
    )
    epochs = mne.Epochs(
        raw, 
        events=all_events.astype(int), 
        event_id=ID_NAMES,
        tmin=TMING_WINDOW[0], 
        tmax=TMING_WINDOW[1],
        baseline=BASELINE,
        preload=True,
        verbose=config.VERBOSE_LEVEL,
        event_repeated='drop'
    )
    
    # Plot evoked potentials for each condition
    for id_event_name, event_id in ID_NAMES.items():
        print(
            f"\nNumber of epochs for {id_event_name}: "
            f"{len(epochs[id_event_name])}"
        )
        evoked = epochs[id_event_name].average(
            by_event_type=True
        )[0]

        # evoked.plot_topo() # interactive plot to see each channel's ERP
        # evoked.plot_image() # plot all channels' ERPs as a heatmap
        
        savefig_path = output_figdir / f"evoked_potential_{labels_map[event_id].replace(' ', '_').lower()}.png"
        evoked_potential_plot(
            evoked=evoked,
            time_window=TMING_WINDOW,
            output_filepath=savefig_path,
            show=False
        )
    
    # Plot difference ERP (target - non-target)
    evoked_target = epochs['listening_bip_target'].average(
        by_event_type=True
    )[0]
    evoked_nontarget = epochs['listening_bip_nontarget'].average(
        by_event_type=True
    )[0]
    evoked_difference = mne.combine_evoked(
        [evoked_target, evoked_nontarget],
        weights=[1, -1]
    )
    savefig_path = output_figdir / f"evoked_potential_listening_bip_difference.png"
    evoked_potential_plot(
        evoked=evoked_difference,
        time_window=TMING_WINDOW,
        output_filepath=savefig_path,
        show=False
    )