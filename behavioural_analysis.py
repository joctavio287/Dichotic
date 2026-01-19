"""
This script processes behavioural data from a PsychoPy experiment.
It extracts metadata, performance and time trial information.
"""
from pathlib import Path
import pandas as pd
import ast

from utils.processing  import (
    dump_dict_to_json
)
from utils.audio_helpers import read_ogg
import config

for subject_file in config.PSYCHOPY_DIR.glob("*.csv"):
    experiment, date, time = subject_file.stem.split("_")[-3:]
    participant_id = subject_file.stem.replace(f"_{experiment}_{date}_{time}", "")
    subject_data = pd.read_csv(subject_file)
    subject_metadata = {
        # 'selected_rows': eval(subject_data.iloc[0]['selected_rows']),
        'selected_rows': ast.literal_eval(subject_data.iloc[0]['selected_rows']),
        'relative_filepath': str(subject_file),
        'participant_id': participant_id,
        'experiment': experiment,
        'date': date,
        'time': time,
        'attended_story': [],
        'audio_filepath': [],
        'audio_filecodes': [],
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
        exp = 'with_probe' if experiment=='DichoticListeningProbe' else 'no_probe'
        if Path(row['audio_filepath']).name.endswith('_short.ogg'):
            audio_file_path = config.STIMULI_DIR / f"processed_audios_short" / Path(row['audio_filepath']).name
        else:
            audio_file_path = config.STIMULI_DIR / f"processed_audios/{exp}" / Path(row['audio_filepath']).name
        audio_filecode = '_'.join(Path(row['audio_filepath']).stem.split('_')[:2])

        # Metadata from listening trials
        subject_metadata['attended_story'].append(int(row['attended_story']))
        subject_metadata['audio_filepath'].append(str(audio_file_path))
        subject_metadata['audio_filecodes'].append(audio_filecode)
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

        # audio_file_path = config.STIMULI_DIR / row['audiobook_filepath'].replace('..\\data\\stimuli\\','')Ge

        # t actual durations vs expected durations
        sample_rate, data = read_ogg(
            audio_file_path,
            return_sample_rate=True
        )
        expected_duration = data.shape[0] / sample_rate
        listening_presentation['expected_audiobook_duration'].append(expected_duration)
    print("Processed behavioural data for participant:", participant_id)
    print("Expected durations vs actual durations (s):")
    print(listening_presentation['expected_audiobook_duration'])
    print(listening_presentation['audiobook_duration'])
    print("\n")
    # Save extracted data to .json files
    dump_dict_to_json(
        filepath=config.BEHAVIOURAL_DIR / f"{participant_id}_behavioural.json",
        data_dict={
            'metadata': subject_metadata,
            'behaviour': subject_behaviour,
            'listening_presentation': listening_presentation
        }
    )
    