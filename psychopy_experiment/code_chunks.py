import os
os.chdir("psychopy_experiment")

# ===============================================>>>>>>>>>>>>
# code_row_selection 
# --> Before Experiment
import serial
port = serial.Serial(
   'COM3', # the port the device is connected to
    baudrate=115200, # speed of communication
    timeout=0
)

# --> Begin Experiment
from psychopy import sound
import pandas as pd
import numpy as np
NUMBER_OF_PAIRS = 7
LETTER_SIZE = .035

# Read conditions, possible stimuli combinations and questionaries
conditions = pd.read_csv(
    "conditions.csv",
    delimiter=',',
    header=0
)
audiobook_questionary = pd.read_csv(
    "audiobook_questionary.csv", 
    delimiter=',',
    header=0
)
audiobook_combinations = pd.read_csv(
    "audiobook_combinations_probes.csv", 
    delimiter=',',
    header=0
)

# Sample conditions 
conditions = conditions.sample(
    n=NUMBER_OF_PAIRS
).reset_index()
# Add 1st number of corresponding pair: 1,3,5,7, ...
conditions['n_story'] = list(
    (np.arange(NUMBER_OF_PAIRS)+1) * 2 - 1
)

# Store in memory audiobooks and relevant parameters
metadata = {
    "attended_stories" : [],
    "audio_filepaths" : [],
    "questionaries" : [],
    "target_labels" : [],
    "book_name" : [],
    "stories_L" : [],
    "stories_R" : [],
    "voices_L" : [],
    "voices_R" : [],
    "targets" : [],
    "audios" : []    
}
for n_r, row in enumerate(conditions.itertuples()):
    # Select audiobook based on condition and story numbers
    filter_A = audiobook_combinations['condition_label']==row.target_label
    filter_B = audiobook_combinations['story_L']==row.n_story
    filter_C = audiobook_combinations['story_R']==row.n_story
    selected_audiobook = audiobook_combinations[
        filter_A & (filter_B | filter_C)
    ].iloc[0]
    
    # Get relevant metadata
    metadata['attended_stories'].append(selected_audiobook[f'story_{row.target}'])
    metadata['audio_filepaths'].append(selected_audiobook['filename'])
    metadata['target_labels'].append(row.target_label)
    metadata['stories_L'].append(selected_audiobook['story_L'])
    metadata['stories_R'].append(selected_audiobook['story_R'])
    metadata['voices_R'].append(selected_audiobook['voice_R'])
    metadata['voices_L'].append(selected_audiobook['voice_L'])
    
    metadata['targets'].append(row.target)
    metadata['audios'].append(
        sound.Sound(selected_audiobook['filename'], hamming=True)
    )
    selected_quest = audiobook_questionary[
           audiobook_questionary['book_number']==metadata['attended_stories'][-1]
        ].iloc[0]
    metadata['book_name'].append(selected_quest['book_name'])
    metadata['questionaries'].append(selected_quest)
    print(
        f"\nAttended story: {metadata['attended_stories'][-1]}"
        f"\nAudio filepath: {metadata['audio_filepaths'][-1]}"
        f"\nAudiobook name: {metadata['book_name'][-1]}"
        f"\nTarget label: {metadata['target_labels'][-1]}"
        f"\nTarget: {metadata['targets'][-1]}"
    )

# Store selected rows in the experiment data    
thisExp.addData(
    'selected_rows', 
    conditions['index']
)

print(conditions)
print(metadata['attended_stories'])
print(metadata['audio_filepaths'])
print(metadata['targets'])
print(metadata['audios'])

# --> Begin Routine
port.write(bytes([int(25)])) #by default this lasts 1 frame
# print(25)

# --> End Routine
port.write(bytes([int(30)]))
# print(30)

# ===============================================>>>>>>>>>>>>
# code_prompt
# --> Begin Routine
port.write(bytes([int(35)]))
# print(35)

# Define condition variables
attended_story = metadata['attended_stories'][condition_trials.thisN]
audio_filepath = metadata['audio_filepaths'][condition_trials.thisN]
target_label = metadata['target_labels'][condition_trials.thisN]
questionary = metadata['questionaries'][condition_trials.thisN]
story_L = metadata['stories_L'][condition_trials.thisN]
story_R = metadata['stories_R'][condition_trials.thisN]
voice_L = metadata['voices_L'][condition_trials.thisN]
voice_R = metadata['voices_R'][condition_trials.thisN]
target = metadata['targets'][condition_trials.thisN]

# Text prompt
flecha, lado = ('<<<', 'IZQUIERDO') if target=='L' else ('>>>', 'DERECHO')

# Define questionary elements
correct_answers = []
questions = []
answers_a = []
answers_b = []
answers_c = []
for i in range(1, 4):
    correct_answer = questionary[f'correct_answer{i}']
    question = questionary[f'question{i}']
    answer_a = questionary[f'answer{i}a']
    answer_b = questionary[f'answer{i}b']
    answer_c = questionary[f'answer{i}c']
    correct_answers.append(correct_answer)
    questions.append(question)
    answers_a.append(answer_a)
    answers_b.append(answer_b)
    answers_c.append(answer_c)  

# --> End Routine
port.write(bytes([int(40)]))
# print(40)

# ===============================================>>>>>>>>>>>>
# code_bip
# --> Begin Routine
if currentLoop.name == "bip_trials1":
    trigger = 45
else:
    trigger = 150

port.write(bytes([int(trigger+currentLoop.thisN*3)]))
#print(int(trigger+currentLoop.thisN*3))

# When the loop reaches the end, there will be no silence added
if currentLoop.thisN == (currentLoop.nTotal - 1):
    final_silence.status = FINISHED

# --> End Routine
port.write(bytes([int(trigger+currentLoop.thisN*3+1)]))
#print(int(trigger+currentLoop.thisN*3+1))

# ===============================================>>>>>>>>>>>>
# code_listening
# --> Begin Routine
# Add to log
thisExp.addData('attended_story', attended_story)
thisExp.addData('audio_filepath', audio_filepath)
thisExp.addData('target_label', target_label)
thisExp.addData('story_L', story_L)
thisExp.addData('story_R', story_R)
thisExp.addData('voice_L', voice_L)
thisExp.addData('voice_R', voice_R)
thisExp.addData('target', target)

audiobook = metadata['audios'][condition_trials.thisN]
port.write(bytes([int(100)])) 
# print(100)

# t is measured since routine start
thisExp.addData("time_audiobook_started",t)
audiobook.play()

# --> Each Frame
# t is measured since routine start
if t >= audiobook.duration:
    continueRoutine = False
    audiobook.stop() 
    port.write(bytes([int(105)]))
    # print(105)
    thisExp.addData("time_audiobook_finished",t)

# --> End Routine # TODO lo saque de end routine y lo movi a each frame
# #port.write(bytes([int(105)]))
# print(105)


# ===============================================>>>>>>>>>>>>
# code_questionary0
# --> Begin Routine
port.write(bytes([int(200+0*3)]))
#print(int(200+0*3))

thisExp.addData(f'correct_answer0', correct_answers[0])
thisExp.addData(f'question0', questions[0])
thisExp.addData(f'answer_a0', answers_a[0])
thisExp.addData(f'answer_b0', answers_b[0])
thisExp.addData(f'answer_c0', answers_c[0])

# --> End Routine
port.write(bytes([int(200+0*3+1)]))
#print(int(200+0*3+1))
# ===============================================>>>>>>>>>>>>
# code_questionary1
# --> Begin Routine
port.write(bytes([int(200+1*3)]))
#print(int(200+1*3))

thisExp.addData(f'correct_answer1', correct_answers[1])
thisExp.addData(f'question1', questions[1])
thisExp.addData(f'answer_a1', answers_a[1])
thisExp.addData(f'answer_b1', answers_b[1])
thisExp.addData(f'answer_c1', answers_c[1])

# --> End Routine
port.write(bytes([int(200+1*3+1)]))
# print(int(200+1*3+1))

# ===============================================>>>>>>>>>>>>
# code_questionary2
# --> Begin Routine
port.write(bytes([int(200+2*3)]))
#print(int(200+2*3))

thisExp.addData(f'correct_answer2', correct_answers[2])
thisExp.addData(f'question2', questions[2])
thisExp.addData(f'answer_a2', answers_a[2])
thisExp.addData(f'answer_b2', answers_b[2])
thisExp.addData(f'answer_c2', answers_c[2])

# --> End Routine
port.write(bytes([int(200+2*3+1)]))
# print(int(200+2*3+1))
# ===============================================>>>>>>>>>>>>
# code_bye

# --> Begin Routine
port.write(bytes([int(230)]))
#print(230)

# --> End Routine
port.write(bytes([int(240)]))
#print(240) 