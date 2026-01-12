"""
This script processes audiobook files by converting them to .ogg format,
adjusting sample rates and combining to audios in a stereo format.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import shutil

from utils.audio_helpers import (
    convert_to_wav, combine_audio_stereo, wav_to_ogg, read_wav, 
    save_wav, scale_audio, plot_audio_profile, create_bip,
    create_attention_probe, create_attention_track,
    scramble_audio, scale_audio_to_relative_db, 
)

# Paths
INTERMEDIATE_AUDIO_DIR = Path('data/intermediate_audios')
OUTPUT_DIR = Path('data/processed_audios')
TABLES_DIR = Path('psychopy_experiment')

INTERMEDIATE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_DIR = Path('data/original_audios')
assert AUDIO_DIR.exists(), f"Audio directory {AUDIO_DIR} does not exist. Please load necessary audio files."

# Create output subdirectories  
no_probe_path = OUTPUT_DIR/'no_probe'
probe_path = OUTPUT_DIR/'with_probe'
no_probe_path.mkdir(parents=True, exist_ok=True)
probe_path.mkdir(parents=True, exist_ok=True)

# Hyperparameters
ABSOLUTE_RELATIVE_ATTENUATION_DB = 10
NUMBER_OF_SCRAMBLE_SEGMENTS = 10
THRESHOLD_DIFF_SECONDS = 10 # seconds
COMMON_SAMPLE_RATE = 48000 # Hz
PROBE_DURATION = .1  # seconds
ATTACK_THRESHOLD = 0.1 # Attack detection in probe profile as percentage of max amplitude
PROBE_TYPE = 1000 # "va"
SCRAMBLED_PROBE = False
OGG_BITRATE = '192k' # standard '64k', '96k', '128k', '160k', '192k', '256k', '320k'

BIP_FREQ = 1000  # Hz
BIP_DUR = 500   # ms
BIP_VOL = -20  # dB

# Create a bip sound for events
create_bip(
    output_file=OUTPUT_DIR/'bip.wav',
    bip_freq=BIP_FREQ,
    bip_dur=BIP_DUR,
    bip_vol=BIP_VOL,
    sample_rate=COMMON_SAMPLE_RATE,
    silence_sides_dur=0,
    number_of_bips=0
)
wav_to_ogg(
    input_wav=OUTPUT_DIR / 'bip.wav',
    output_ogg=OUTPUT_DIR / 'bip.ogg',
    sample_rate_target=COMMON_SAMPLE_RATE,
    bitrate=OGG_BITRATE
)
(OUTPUT_DIR / 'bip.wav').unlink()

# Get total number of audios
audio_paths = list(AUDIO_DIR.glob('*.mp3'))
assert len(audio_paths)%2==0, "The number of audio files must be even. One male, one female"
number_of_stories = len(audio_paths)//2

# Find male and female with corresponding numbers
ordered_female = sorted(
    [path for path in audio_paths if 'mujer' in path.name],
    key=lambda p: p.name.split('_')[0]
)
ordered_male = sorted(
    [path for path in audio_paths if 'hombre' in path.name],
    key=lambda p: p.name.split('_')[0]
)
audio_names = [f_path.stem.split('_')[1] for f_path in ordered_female]
assert audio_names == [m_path.stem.split('_')[1] for m_path in ordered_male], "Mismatch between female and male audio names"

# Get combinations with consecutive order 1,2 ; 3,4 ; 5,6; etc
combinations = []
for i in range(number_of_stories):
    if i % 2 == 0:
        f_path = ordered_female[i]
        m_path = ordered_male[i + 1]
        combinations.append(
            (f_path, m_path)
        )
        m_path = ordered_male[i]
        f_path = ordered_female[i + 1]
        combinations.append(
            (f_path, m_path)
        )

# Create attentional probe
attention_probe_path = OUTPUT_DIR / 'attention_probe.wav'
scrambled_probe_path = attention_probe_path.with_name(attention_probe_path.stem + '_scrambled.wav')
create_attention_probe(
    output_attention_probe_path=attention_probe_path,
    duration_seconds=PROBE_DURATION,
    stimulus_type=PROBE_TYPE,
    sr=COMMON_SAMPLE_RATE
)
# Generate audio profile to verify attack characteristics (should be fast and clear)
probe_profile_path = attention_probe_path.parents[1] / f'attention_probe_{PROBE_TYPE}_{int(PROBE_DURATION*1000)}_profile.png'
attack_metrics = plot_audio_profile(
    audio_path=attention_probe_path,
    output_path=probe_profile_path,
    attack_threshold=ATTACK_THRESHOLD,
    plot_spectrum=True
)
if isinstance(PROBE_TYPE, str) and SCRAMBLED_PROBE:
    scramble_audio(
        input_file=attention_probe_path,
        output_file=scrambled_probe_path,
        number_of_segments=NUMBER_OF_SCRAMBLE_SEGMENTS
    )
    attention_probe_path = scrambled_probe_path

# Process each combination
df_audio_combinations = []
df_audio_combinations_noprobes = []

skipped_combinations = []
for j, (audio_f, audio_m) in enumerate(combinations):
    # Get numbers and names of the stories
    number_f, audio_name_f = int(audio_f.stem.split('_')[0]), audio_f.stem.split('_')[1]
    number_m, audio_name_m = int(audio_m.stem.split('_')[0]), audio_m.stem.split('_')[1]

    # The code names are based on the original numbering of the stories 
    stereo_name1 = f'F{number_f:02d}_M{number_m:02d}' 
    stereo_name2 = f'M{number_m:02d}_F{number_f:02d}' 
    
    # Examples:
    # First iteration: (number_f, number_m) = (1, 2)
    # F01_M02.wav --> female story 1 on left ear, male story 2 on right ear
    # M02_F01.wav --> male story 2 on left ear, female story 1 on right ear
    # Second iteration: (number_f, number_m) = (2, 1)
    # F02_M01.wav --> female story 2 on left ear, male story 1 on right ear
    # M01_F02.wav --> male story 1 on left ear, female story 2 on right ear
    # ...

    # Convert to wav to operate on higher quality audio --> then downsample if needed
    convert_to_wav(audio_f, INTERMEDIATE_AUDIO_DIR / audio_f.with_suffix('.wav').name, exists_ok=True, sample_rate_target=COMMON_SAMPLE_RATE)
    convert_to_wav(audio_m, INTERMEDIATE_AUDIO_DIR / audio_m.with_suffix('.wav').name, exists_ok=True, sample_rate_target=COMMON_SAMPLE_RATE)
    audio_f = INTERMEDIATE_AUDIO_DIR / audio_f.with_suffix('.wav').name
    audio_m = INTERMEDIATE_AUDIO_DIR / audio_m.with_suffix('.wav').name
    
    # Verify audio sample lengths and sample rates
    (sr_m, wav_m), (sr_f, wav_f) = read_wav(audio_m, return_sample_rate=True), read_wav(audio_f, return_sample_rate=True)
    assert sr_m == sr_f, "Sample rates of male and female mismatch"
    len_m, len_f = len(wav_m), len(wav_f) 
    
    # Skip combinations with length differences beyond threshold
    diff = len_m - len_f
    if abs(diff) > THRESHOLD_DIFF_SECONDS*sr_m:
        skipped_combinations.append((stereo_name1, stereo_name2))
        print(
            f"\n\n\t\tAudio lengths in combination {number_f}_{audio_name_f}_F-{number_m}_{audio_name_m}_M"+\
            f" differ by {diff/sr_m:.2f}s, "+\
            f"which is more than the current threshold ({THRESHOLD_DIFF_SECONDS} s)\n\n"+\
            "\t\tSkipping these 2 combinations.\n\n"
        )
        continue
    # Else, split differences, contracting longer audio and dilating shorter audio
    else:
        scale_audio(
            input_file=audio_m,
            output_file=audio_m,
            delta_frames=-diff//2 if diff >=0 else -diff//2
        )
        scale_audio(
            input_file=audio_f,
            output_file=audio_f,
            delta_frames=diff//2 if diff >=0 else diff//2
        )
    
    # Rescale female and male voices to common dB level
    scale_audio_to_relative_db(
        audio_to_scale_path=audio_f,
        reference_audio_path=audio_m,
        target_db_diff=0 # dB
    )

    # For each combination, first create stereo audio without probes 
    for i, stereo_name in enumerate([stereo_name1, stereo_name2]):
        audio_left = audio_f if i==0 else audio_m
        audio_right = audio_m if i==0 else audio_f
        combine_audio_stereo(
            audio_left=audio_left,
            audio_right=audio_right,
            output_file=no_probe_path / f'{stereo_name}_no_probe.wav'
        )

        # Now redefine audios with ABSOLUTE_RELATIVE_ATTENUATION_DB attenuation
        scale_audio_to_relative_db(
            audio_to_scale_path=no_probe_path / f'{stereo_name}_no_probe.wav',
            reference_audio_path=attention_probe_path,
            target_db_diff=-ABSOLUTE_RELATIVE_ATTENUATION_DB # dB
        )

        # Convert to ogg
        wav_to_ogg(
            input_wav=no_probe_path / f'{stereo_name}_no_probe.wav',
            output_ogg=no_probe_path / f'{stereo_name}_no_probe.ogg',
            sample_rate_target=COMMON_SAMPLE_RATE,
            bitrate=OGG_BITRATE
        )
        
        # Then add attention tracks
        sr_data, data = read_wav(no_probe_path / f'{stereo_name}_no_probe.wav', return_sample_rate=True)
        normalized_data = data / np.max(np.abs(data))

        n_probes, track_left, track_right, left_onsets, right_onsets = create_attention_track(
            duration_samples=len(data),
            sr=COMMON_SAMPLE_RATE,
            probe_audio_path=attention_probe_path,
            return_onsets=True
        )
        print(f'Added {n_probes} probes to {stereo_name}')
        normalized_data[:,0] += track_left
        normalized_data[:,1] += track_right
        
        # Save final audios according to hyperparameters
        if isinstance(PROBE_TYPE, str) and SCRAMBLED_PROBE:
            save_path = probe_path / f'{stereo_name}_scrambled.wav'
        elif isinstance(PROBE_TYPE, str) and not SCRAMBLED_PROBE:
            save_path = probe_path / f'{stereo_name}_not_scrambled.wav'
        elif isinstance(PROBE_TYPE, int):
            save_path = probe_path / f'{stereo_name}_tone_probe.wav'
        save_wav(save_path, sr_data, normalized_data)

        # Save probe onsets on a csv file
        data_onsets = pd.DataFrame({
            'left_s': left_onsets,
            'right_s': right_onsets
        })
        onsets_path = save_path.parents[1] / 'onsets'
        onsets_path.mkdir(parents=True, exist_ok=True)
        data_onsets.to_csv(
            onsets_path / f'{stereo_name}_onsets.csv',
            index=False,
            sep=',',
            float_format='%.6f'
        )
        
        # Convert to ogg
        wav_to_ogg(
            input_wav=save_path,
            output_ogg=save_path.with_suffix('.ogg'),
            sample_rate_target=COMMON_SAMPLE_RATE,
            bitrate=OGG_BITRATE
        )
    
        # Save combinations
        story_right = stereo_name.split('_')[1][1:]
        story_left = stereo_name.split('_')[0][1:]
        voice_right = stereo_name.split('_')[1][0]
        voice_left = stereo_name.split('_')[0][0]
        ordered = story_left < story_right
        condition_label = f'O_{voice_left}_{voice_right}' if ordered else f'NO_{voice_left}_{voice_right}'
        
        df_audio_combinations.append({
            'filename':str(Path("..")/save_path.with_suffix('.ogg')),
            'condition_label': condition_label,
            'ordered': ordered,
            'story_L': int(number_f),
            'story_R': int(number_m),
            'voice_L': voice_left,
            'voice_R': voice_right,
        })
        df_audio_combinations_noprobes.append({
            'filename': str(Path("..")/ no_probe_path / f'{stereo_name}_no_probe.ogg'),
            'condition_label': condition_label,
            'ordered': ordered,
            'story_L': int(number_f),
            'story_R': int(number_m),
            'voice_L': voice_left,
            'voice_R': voice_right
        })
    
# Print summary
print(f'\n\nExpected number of combinations: {len(combinations) * 2}')
print(f'Actual number of saved combinations: {len(df_audio_combinations)}\n\n')

# Create csv with filenames relative to psychopy experiment folder and it's labels
csv_audio_combinations_no_probes_path = TABLES_DIR / 'audiobook_combinations_no_probes.csv'
csv_audio_combinations_path = TABLES_DIR / 'audiobook_combinations_probes.csv'
df_audio_combinations = pd.DataFrame(df_audio_combinations)
df_noprobes = pd.DataFrame(df_audio_combinations_noprobes)
df_audio_combinations.to_csv(csv_audio_combinations_path, index=False)
df_noprobes.to_csv(csv_audio_combinations_no_probes_path, index=False)

# Remove .wav files from processed folders to keep only ogg outputs
no_probe_dir = OUTPUT_DIR / 'no_probe'
with_probe_dir = OUTPUT_DIR / 'with_probe'
for d in (no_probe_dir, with_probe_dir):
    if d.exists():
        for wav_file in d.glob('*.wav'):
            try:
                wav_file.unlink()
            except Exception:
                pass
# Delete intermediate files
shutil.rmtree(INTERMEDIATE_AUDIO_DIR)