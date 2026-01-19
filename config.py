from pathlib import Path
import mne

BEHAVIOURAL_DIR = Path("data/behavioural_data")
STIMULI_DIR = Path("data/stimuli")
EEG_DIR = Path("data/EEG/raw_eeg")
ONSETS_DIR = STIMULI_DIR / "processed_audios/onsets"
PREPROCESSED_DIR = EEG_DIR.parent / "preprocessed"

PSYCHOPY_DIR = Path("psychopy_experiment/data")
FIGURES_DIR = Path("figures")


VERBOSE_LEVEL = 'CRITICAL'
UNUSED_EXT_CH = ['EXG6', 'EXG7', 'EXG8']
TARGET_SAMPLING_RATE = 512  # Hz
ICA_PERCENTAGE = 0.98  
RANDOM_SEED = 42
TRIGGER_IDS = {
    'listening': (100, 105), # start and end triggers for listening periods
    'bips1': (45, 3, 10), # start, step, number of bips for first block
    'bips2': (150, 3, 10)  # start, step, number of bips for second block
}

# Rename EEG channels to standard 10-20 names
BIOSEMI_MAPPING = {
    old: new for old, new in zip(
        [f'A{j}' for j in range(1,33)]+[f'B{k}' for k in range(1,33)], 
        mne.channels.make_standard_montage('biosemi64').ch_names
    )
}
EXTERNAL_MAPPING = {
    'EXG1':'M1','EXG2':'M2','EXG3':'HEOG1','EXG4':'HEOG2', 
    'EXG5':'VEOG1','Status':'Triggers'
}
CH_TYPES = {
    'M1':'eeg','M2':'eeg', 'HEOG1':'eog','HEOG2':'eog',
    'VEOG1':'eog','Triggers':'stim'
}

ICA_REMOVAL = {
    'pruebapiloto_ed_1': [0, 7, 12, 13, 14, 15, 16, 18, 19, 20, 22, 23],
}

USE_SCIENCE_PLOTS = False