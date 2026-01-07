"""
This script processes audiobook files by converting them to WAV format,
adjusting sample rates and combining to audios in a stereo format.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import shutil
import ffmpeg
import csv

from utils.audio_helpers import (
    read_wav, save_wav, get_sample_rate, scale_audio,
    create_attention_probe, create_attention_track,
    convert_to_wav, combine_audio_stereo, scramble_audio,
    scale_audio_to_relative_db, plot_audio_profile
)

INTERMEDIATE_AUDIO_DIR = Path('data/intermediate_audios')
AUDIO_DIR = Path('data/original_audios')
OUTPUT_DIR = Path('data/processed_audios')
TABLES_DIR = Path('psychopy_experiment')
TABLES_DIR.mkdir(parents=True, exist_ok=True)
ABSOLUTE_RELATIVE_ATTENUATION_DB = 10
NUMBER_OF_SCRAMBLE_SEGMENTS = 10
THRESHOLD_DIFF_SECONDS = 10 # seconds
COMMON_SAMPLE_RATE = 48000 # Hz
PROBE_DURATION = .1  # seconds
ATTACK_THRESHOLD = 0.1 # Attack detection in probe profile as percentage of max amplitude
PROBE_TYPE = 1000 # "va"
SCRAMBLED_PROBE = False

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

INTERMEDIATE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
saved_combinations_clean = []
saved_combinations = []

skipped_combinations = []
combinations
for j, (audio_f, audio_m) in enumerate(combinations):
    number_f, audio_name_f = int(audio_f.stem.split('_')[0]), audio_f.stem.split('_')[1]
    number_m, audio_name_m = int(audio_m.stem.split('_')[0]), audio_m.stem.split('_')[1]

    # A_sideL_voiceF
    order = 'AB' if number_f < number_m else 'BA'
    stereo_name1 = f'{number_f:02d}_{number_m:02d}_FL_MR_{order}'
    stereo_name2 = f'{number_f:02d}_{number_m:02d}_FR_ML_{order}'

    # Convert to wav
    convert_to_wav(audio_f, INTERMEDIATE_AUDIO_DIR / audio_f.with_suffix('.wav').name, exists_ok=True, sample_rate_target=COMMON_SAMPLE_RATE)
    convert_to_wav(audio_m, INTERMEDIATE_AUDIO_DIR / audio_m.with_suffix('.wav').name, exists_ok=True, sample_rate_target=COMMON_SAMPLE_RATE)
    audio_f = INTERMEDIATE_AUDIO_DIR / audio_f.with_suffix('.wav').name
    audio_m = INTERMEDIATE_AUDIO_DIR / audio_m.with_suffix('.wav').name
    
    # Verify audio lengths 
    sr_m, sr_f = get_sample_rate(audio_m), get_sample_rate(audio_f)
    assert sr_m == sr_f, "Sample rates of male and female audios must match"
    wav_m, wav_f = read_wav(audio_m), read_wav(audio_f)
    len_m, len_f = len(wav_m), len(wav_f) # in samples
    diff = len_m - len_f
    if abs(diff) > THRESHOLD_DIFF_SECONDS*sr_m:
        skipped_combinations.append((stereo_name1, stereo_name2))
        print(
            f"\n\n\t\tAudio lengths in combination {number_f}_{audio_name_f}_mujer-{number_m}_{audio_name_m}_hombre differ by {diff/sr_m:.2f}s, "+\
            f"which is more than the current threshold ({THRESHOLD_DIFF_SECONDS} s)\n\n"+\
            "\t\tSkipping these 2 combinations.\n\n"
        )
        continue

    # Split differences, contracting longer audio and dilating shorter audio
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
    # Combine to stereo and rescale to relative dB
    no_probe_path = OUTPUT_DIR/'no_probe'
    no_probe_path.mkdir(parents=True, exist_ok=True)
    combine_audio_stereo(
        audio_left=audio_f,
        audio_right=audio_m,
        output_file=no_probe_path / f'{stereo_name1}_no_probe.wav'
    )
    scale_audio_to_relative_db(
        audio_to_scale_path=no_probe_path / f'{stereo_name1}_no_probe.wav',
        reference_audio_path=attention_probe_path,
        target_db_diff=-ABSOLUTE_RELATIVE_ATTENUATION_DB # dB
    )
    combine_audio_stereo(
        audio_left=audio_m,
        audio_right=audio_f,
        output_file=no_probe_path / f'{stereo_name2}_no_probe.wav'
    )
    scale_audio_to_relative_db(
        audio_to_scale_path=no_probe_path / f'{stereo_name2}_no_probe.wav',
        reference_audio_path=attention_probe_path,
        target_db_diff=-ABSOLUTE_RELATIVE_ATTENUATION_DB # dB
    )
    
    # Add attention tracks
    sr_data, data1 = read_wav(no_probe_path / f'{stereo_name1}_no_probe.wav', return_sample_rate=True)
    sr_data, data2 = read_wav(no_probe_path / f'{stereo_name2}_no_probe.wav', return_sample_rate=True)

    normalized_data1 = data1 / np.max(np.abs(data1))
    normalized_data2 = data2 / np.max(np.abs(data2))
    n_probes1, track_left1, track_right1, left_onsets, right_onsets = create_attention_track(
        duration_samples=len(data1),
        sr=COMMON_SAMPLE_RATE,
        probe_audio_path=attention_probe_path,
        return_onsets=True
    )
    n_probes2, track_left2, track_right2, left_onsets2, right_onsets2 = create_attention_track(
        duration_samples=len(data2),
        sr=COMMON_SAMPLE_RATE,
        probe_audio_path=attention_probe_path,
        return_onsets=True
    )

    print(f'Added {n_probes1} probes to {stereo_name1}, and {n_probes2} probes to {stereo_name2}')
    normalized_data1[:,0] += track_left1
    normalized_data2[:,0] += track_left2
    normalized_data1[:,1] += track_right1
    normalized_data2[:,1] += track_right2
    
    # Save final audios
    probe_path = OUTPUT_DIR/'with_probe'
    probe_path.mkdir(parents=True, exist_ok=True)
    if isinstance(PROBE_TYPE, str) and SCRAMBLED_PROBE:
        save_path1 = probe_path / f'{stereo_name1}_scrambled.wav'
        save_path2 = probe_path / f'{stereo_name2}_scrambled.wav'
    elif isinstance(PROBE_TYPE, str) and not SCRAMBLED_PROBE:
        save_path1 = probe_path / f'{stereo_name1}_not_scrambled.wav'
        save_path2 = probe_path / f'{stereo_name2}_not_scrambled.wav'
    if isinstance(PROBE_TYPE, int):
        save_path1 = probe_path / f'{stereo_name1}_tone_probe.wav'
        save_path2 = probe_path / f'{stereo_name2}_tone_probe.wav'
    save_wav(save_path1, sr_data, normalized_data1)
    save_wav(save_path2, sr_data, normalized_data2)
    # Save onsets on a txt file
    onsets_path1 = save_path1.parent / 'onsets'
    onsets_path1.mkdir(parents=True, exist_ok=True)
    with open(onsets_path1 / f'{stereo_name1}_onsets.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['left_s', 'right_s'])
        max_len = max(len(left_onsets), len(right_onsets))
        for i in range(max_len):
            l = f'{left_onsets[i]:.3f}' if i < len(left_onsets) else ''
            r = f'{right_onsets[i]:.3f}' if i < len(right_onsets) else ''
            writer.writerow([l, r])
    onsets_path2 = save_path2.parent / 'onsets'
    onsets_path2.mkdir(parents=True, exist_ok=True)
    with open(onsets_path2 / f'{stereo_name2}_onsets.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['left_s', 'right_s'])
        max_len = max(len(left_onsets2), len(right_onsets2))
        for i in range(max_len):
            l = f'{left_onsets2[i]:.3f}' if i < len(left_onsets2) else ''
            r = f'{right_onsets2[i]:.3f}' if i < len(right_onsets2) else ''
            writer.writerow([l, r])
    
    # Convert to ogg
    for input_file, output_file, sample_rate_target in [
        (no_probe_path / f'{stereo_name1}_no_probe.wav', no_probe_path / f'{stereo_name1}_no_probe.ogg', COMMON_SAMPLE_RATE),
        (no_probe_path / f'{stereo_name2}_no_probe.wav', no_probe_path / f'{stereo_name2}_no_probe.ogg', COMMON_SAMPLE_RATE),
        (save_path1, save_path1.with_suffix('.ogg'), COMMON_SAMPLE_RATE),
        (save_path2, save_path2.with_suffix('.ogg'), COMMON_SAMPLE_RATE)
    ]:
        try:
            if not Path(input_file).exists():
                print(f"Input file missing, skipping: {input_file}")
                continue

            (
                ffmpeg
                .input(str(input_file))
                .output(
                    str(output_file),
                    format='ogg',
                    acodec='libopus', # O 'libopus' si tienes una versión muy nueva de ffmpeg
                    ar=sample_rate_target,
                    ac=2,
                    audio_bitrate='192k'
                )
                .overwrite_output()
                .run(quiet=True)
            )
            if not Path(output_file).exists():
                print(f"Output file missing, skipping: {output_file}")
                continue
        except ffmpeg.Error as e:
            stderr = getattr(e, 'stderr', None)
            msg = stderr.decode() if isinstance(stderr, (bytes, bytearray)) else str(e)
            print(f'ffmpeg error converting {input_file} -> {output_file}: {msg}')
    saved_combinations.append((save_path1.with_suffix('.ogg'), save_path2.with_suffix('.ogg')))
    saved_combinations_clean.append((no_probe_path / f'{stereo_name1}_no_probe.ogg', no_probe_path /
                                        f'{stereo_name2}_no_probe.ogg'))
    
# In the ideal case, where no combination is exluded due to length differences, the total number
# of saved combinations should be number_of_stories*(number_of_stories-1)*2 because each story c
# an be combined with (number_of_stories-1) stories of the other gender and be played either in 
# left or right ear.
# expected_number_of_combinations = number_of_stories * (number_of_stories - 1) * 2
expected_number_of_combinations = len(combinations) * 2
print(f'\n\nExpected number of combinations: {expected_number_of_combinations}')
print(f'Actual number of saved combinations: {len(saved_combinations)*2}\n\n')

# Create csv with filenames relative to psychopy experiment folder and it's labels
df_rows = []
for save_path1, save_path2 in saved_combinations:
    df_rows.append({
        'filename':str(Path("..")/save_path1),
        'condition_label': '_'.join(save_path1.name.split('_')[2:5]),
        'number_story_A': int(save_path1.name.split('_')[0]),
        'number_story_B': int(save_path1.name.split('_')[1])
    })
    df_rows.append({
        'filename': str(Path("..")/save_path2),
        'condition_label': '_'.join(save_path2.name.split('_')[2:5]),
        'number_story_A': int(save_path2.name.split('_')[0]),
        'number_story_B': int(save_path2.name.split('_')[1])
    })
df = pd.DataFrame(df_rows)
csv_path = TABLES_DIR / 'audiobook_combinations_probes.csv'
df.to_csv(csv_path, index=False)

df_rows_clean = []
for stereo_name1, stereo_name2 in saved_combinations_clean:
    df_rows_clean.append({
        'filename': str(Path("..")/stereo_name1),
        'condition_label': '_'.join(stereo_name1.name.split('_')[2:5]),
        'number_story_A': int(stereo_name1.name.split('_')[0]),
        'number_story_B': int(stereo_name1.name.split('_')[1])
    })
    df_rows_clean.append({
        'filename': str(Path("..")/stereo_name2),
        'condition_label': '_'.join(stereo_name2.name.split('_')[2:5]),
        'number_story_A': int(stereo_name2.name.split('_')[0]),
        'number_story_B': int(stereo_name2.name.split('_')[1])
    })
df_clean = pd.DataFrame(df_rows_clean)
csv_path_clean = TABLES_DIR / 'audiobook_combinations_no_probes.csv'
df_clean.to_csv(csv_path_clean, index=False)

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