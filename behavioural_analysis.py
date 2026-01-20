"""
This script processes behavioural data from a PsychoPy experiment.
It extracts metadata, performance and time trial information.
"""
import matplotlib.pyplot as plt 
from pathlib import Path
import seaborn as sns
import pandas as pd
import numpy as np
import ast

from utils.processing  import (
    dump_dict_to_json, load_json_to_dict
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
    for j, row in subject_data.iterrows():
        exp = 'with_probe' if experiment=='DichoticListeningProbe' else 'no_probe'
        
        if Path(row['audio_filepath']).name.endswith('_short.ogg'):
            audio_file_path = config.STIMULI_DIR / f"processed_audios_short" / Path(row['audio_filepath']).name
        else:
            # Check consistency of audio file paths
            if exp == 'with_probe' and not Path(row['audio_filepath']).parent.name == 'with_probe':
                raise ValueError(f"Inconsistent audio file path or name of experiment {experiment}: {row['audio_filepath']}")
            elif exp == 'no_probe' and not Path(row['audio_filepath']).parent.name == 'no_probe':
                raise ValueError(f"Inconsistent audio file path or name of experiment {experiment}: {row['audio_filepath']}")
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
    
    # Test whether the listening['expected_audiobook_duration'] differ from actual durations in an even number of samples
    frame_rate = np.mean(subject_metadata['framerate'])
    duration_diff = (
        np.array(listening_presentation['expected_audiobook_duration']) - np.array(listening_presentation['audiobook_duration'])
    )
    duration_diff_samples = np.abs(np.round(duration_diff * frame_rate).astype(int))

    print("\tProcessed behavioural data for participant:", participant_id)
    print("\n\tDifference between actual and expected durations of audiobooks (in frames):\n")
    print("\t\t", duration_diff_samples)
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

# ========================================================================
# Aggregate behavioural data across participants for analysis and plotting

# Compile all participants scores into a single DataFrame
score_rows = []
for subj_json in config.BEHAVIOURAL_DIR.glob("*_behavioural.json"):
    data = load_json_to_dict(subj_json)
    pid = data["metadata"]["participant_id"]
    scores = data["behaviour"]["questionary_evaluations"]
    score_rows.extend(
        {"correct": bool(v), "question_index": i % 3, "participant": pid}
        for i, v in enumerate(scores)
    )
scores_data = pd.DataFrame(score_rows)
scores_data.to_csv(
    config.BEHAVIOURAL_DIR / "all_participants_behavioural_data.csv",
    index=False
)

# Disaggregate scores by participant and question index
scores_by_participant = (
    scores_data
        .rename(columns={"correct": r"Score Accuracy [$\%$]"})
        .assign(**{r"Score Accuracy [$\%$]": lambda df: df[r"Score Accuracy [$\%$]"] * 1e2})
        .groupby("participant", as_index=False)[r"Score Accuracy [$\%$]"]
        .mean()
)
summary = (
    scores_data
        .groupby("question_index", as_index=False)["correct"]
        .agg(mean="mean", sem=lambda s: s.std(ddof=1) / np.sqrt(s.count()))
        # .agg(mean="mean", sem="sem")
)

# Plot behavioural performance across participants
fig_path = config.FIGURES_DIR / "behavioural" / "performance_across_participants.png"
fig_path.parent.mkdir(parents=True, exist_ok=True)

behavioural_fig, axes = plt.subplots(
    nrows=2, ncols=1,
    figsize=(8, 6),
    tight_layout=True
)
behavioural_fig.suptitle("Behavioural performance across participants", fontsize=12)
histogram_plot = sns.histplot(
    scores_by_participant[r"Score Accuracy [$\%$]"], 
    bins=10, 
    kde=False, 
    # stat="count",
    color='green',
    alpha=0.4,
    ax=axes[0]
)
_ = histogram_plot.axes.set_ylabel("Number of participants")
_ = histogram_plot.axes.grid(True)

stripplot = sns.stripplot(
    data=scores_data, 
    x="question_index", 
    y="correct", 
    color="black", 
    alpha=0.3, 
    jitter=0.2,
    ax=axes[1]
)
errorbars = axes[1].errorbar(
    summary["question_index"],
    summary["mean"],
    yerr=summary["sem"],
    fmt="o",
    color="black",
    capsize=4,
    linewidth=1,
    zorder=5
)
_ = axes[1].legend(
    [errorbars], 
    ["Mean ± SEM"], 
    loc=(.58, 0.45)
)
_ = axes[1].set_xlabel("Question Index")
_ = axes[1].set_ylabel("Score(0=incorrect, 1=correct)")
_ = axes[1].grid(
    axis='y',
    which='major',
)

behavioural_fig.savefig(
    fig_path,
    dpi=300
)
print(f"\tSaved behavioural figure in {fig_path.parent}")