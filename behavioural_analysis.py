"""
This script processes behavioural data from a PsychoPy experiment.
It extracts metadata, performance and time trial information.
"""
from pathlib import Path
import pandas as pd
import numpy as np

from utils.audio_helpers import read_ogg

BEHAVIOURAL_DIR = Path("psychopy_experiment/data")
for subject_file in BEHAVIOURAL_DIR.glob("*.csv"):
    participant_id, experiment, date, time = subject_file.stem.split("_")
    subject_data = pd.read_csv(subject_file)
    subject_metadata = {
        'selected_rows': eval(subject_data.iloc[0]['selected_rows']),
        'relative_filepath': str(subject_file),
        'participant_id': participant_id,
        'experiment': experiment,
        'date': date,
        'time': time,
        'attended_story': [],
        'audio_filepath': [],
        'framerate': [],
        'condition': [],
        'story_L': [], 
        'voice_L': [], 
        'story_R': [],
        'voice_R': [],
        'target': [],
    }
    subject_behaviour = {
        'questionary_answers': [],
        'questionary_rts': [],
        'questionary_evaluations': []
    }
    listening_presentation = {
        'expected_audiobook_duration': [],
        'time_audiobook_finished': [],
        'time_audiobook_started': [],
        'audiobook_duration': [],
    }

    # First and last rows contain metadata (start and end prompts)
    subject_data = subject_data.iloc[1:-1]

    # Separate questionary and listening trials (rows)
    answers_column = 'questions_trial.key_resp_questionary.keys'
    for j, row in subject_data.iterrows():
        # Metadata from listening trials
        subject_metadata['attended_story'].append(int(row['attended_story']))
        subject_metadata['audio_filepath'].append(row['audio_filepath'])
        subject_metadata['condition'].append(row['target_label'])
        subject_metadata['framerate'].append(row['frameRate'])
        subject_metadata['story_L'].append(int(row['story_L']))
        subject_metadata['story_R'].append(int(row['story_R']))
        subject_metadata['voice_L'].append(row['voice_L'])
        subject_metadata['voice_R'].append(row['voice_R'])
        subject_metadata['target'].append(row['target'])

        # Behavioural data from questionary trials
        for k in range(3):
            answer = row[f'key_resp_questionary{k}.keys']
            subject_behaviour['questionary_evaluations'].append(answer==row[f'correct_answer{k}'])
            subject_behaviour['questionary_rts'].append(row[f'key_resp_questionary{k}.rt'])
            subject_behaviour['questionary_answers'].append(answer)
        
        # Timing data from listening trials
        listening_presentation['time_audiobook_finished'].append(row['time_audiobook_finished'])
        listening_presentation['time_audiobook_started'].append(row['time_audiobook_started'])
        listening_presentation['audiobook_duration'].append(
            row['time_audiobook_finished'] - row['time_audiobook_started']
        )

        # Get actual durations vs expected durations
        sample_rate, data = read_ogg(
            row['audio_filepath'].replace('..\\',''), # adjust relative path to cwd
            return_sample_rate=True
        )
        expected_duration = data.shape[0] / sample_rate
        listening_presentation['expected_audiobook_duration'].append(expected_duration)

    # Contrast real time durations of audiobook presentations with expected durations
    listening_presentation['audiobook_duration'] = np.array(listening_presentation['audiobook_duration'])
    listening_presentation['expected_audiobook_duration'] = np.array(listening_presentation['expected_audiobook_duration'])

    print(listening_presentation['expected_audiobook_duration'], listening_presentation['audiobook_duration'])
