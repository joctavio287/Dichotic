"""
This script processes audiobook files by converting them to WAV format,
adjusting sample rates and combining to audios in a stereo format.
"""
from pathlib import Path
import numpy as np

from utils.audio_helpers import (
    read_wav, save_wav, get_sample_rate, scale_audio,
    create_attention_probe, create_attention_track,
    convert_to_wav, combine_audio_stereo, scramble_audio,
    scale_audio_to_relative_db
)

INTERMEDIATE_AUDIO_DIR = Path('data/intermediate_audios')
AUDIO_DIR = Path('data/original_audios')
OUTPUT_DIR = Path('data/processed_audios')
ABSOLUTE_RELATIVE_ATTENUATION_DB = 20
NUMBER_OF_SCRAMBLE_SEGMENTS = 10
THRESHOLD_DIFF_SECONDS = 10 # seconds
COMMON_SAMPLE_RATE = 44100 # Hz
PROBE_DURATION = 0.1  # seconds
SCRAMBLED_PROBE = True

INTERMEDIATE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Get total number of audios
audio_paths = list(AUDIO_DIR.glob('*.mp3'))
assert len(audio_paths)%2==0, "The number of audio files must be even. One male, one female"
number_of_audios_pairs = len(audio_paths)//2

# Find male and female with corresponding numbers
ordered_female = sorted(
    [path for path in audio_paths if 'mujer' in path.name],
    key=lambda p: p.name.split('_')[0]
)
ordered_male = sorted(
    [path for path in audio_paths if 'hombre' in path.name],
    key=lambda p: p.name.split('_')[0]
)

# Get combinatins that doesn't match in name
combinations = []
for f_path in ordered_female:
    audio_name_f = f_path.stem.split('_')[1]
    for m_path in ordered_male:
        audio_name_m = m_path.stem.split('_')[1]
        if audio_name_f != audio_name_m:
            combinations.append((f_path, m_path))
        else:
            continue

# Create attentional probe
attention_probe_path = OUTPUT_DIR / 'attention_probe.wav'
scrambled_probe_path = attention_probe_path.with_name(attention_probe_path.stem + '_scrambled.wav')
if not attention_probe_path.exists():
    create_attention_probe(
        output_attention_probe_path=attention_probe_path,
        duration_seconds=PROBE_DURATION,
        text="va",
        sr=COMMON_SAMPLE_RATE
    )
    scramble_audio(
        input_file=attention_probe_path,
        output_file=scrambled_probe_path,
        number_of_segments=NUMBER_OF_SCRAMBLE_SEGMENTS
    )
if SCRAMBLED_PROBE:
    attention_probe_path = scrambled_probe_path
#TODO hacer perfil del audio para ver el ataque: tiene que ser rápido y claro

# Combinaciones de audios cruzados siempre--> ver todas las combinaciones? No superpuestos # TODO futuro emparejar por longitud asi la distorsion es lo mas chica posible
for j, (audio_f, audio_m) in enumerate(combinations):
    number_f, audio_name_f = int(audio_f.stem.split('_')[0]), audio_f.stem.split('_')[1]
    number_m, audio_name_m = int(audio_m.stem.split('_')[0]), audio_m.stem.split('_')[1]
    stereo_name1 = f'{number_f:02d}_{audio_name_f}_mujer_izquierda_{number_m:02d}_{audio_name_m}_hombre_derecha'
    stereo_name2 = f'{number_f:02d}_{audio_name_f}_mujer_derecha_{number_m:02d}_{audio_name_m}_hombre_izquierda'

    # Convert to wav
    convert_to_wav(audio_f, INTERMEDIATE_AUDIO_DIR / audio_f.with_suffix('.wav').name, exists_ok=True)
    convert_to_wav(audio_m, INTERMEDIATE_AUDIO_DIR / audio_m.with_suffix('.wav').name, exists_ok=True)
    audio_f = INTERMEDIATE_AUDIO_DIR / audio_f.with_suffix('.wav').name
    audio_m = INTERMEDIATE_AUDIO_DIR / audio_m.with_suffix('.wav').name
    
    # Verify audio lengths 
    sr_m, sr_f = get_sample_rate(audio_m), get_sample_rate(audio_f)
    assert sr_m == sr_f, "Sample rates of male and female audios must match"
    wav_m, wav_f = read_wav(audio_m), read_wav(audio_f)
    len_m, len_f = len(wav_m), len(wav_f) # in samples
    diff = len_m - len_f
    if abs(diff) > THRESHOLD_DIFF_SECONDS*sr_m:
        print(
            f"\n\nAudio lengths in combination {audio_name_f}_mujer-{audio_name_m}_hombre differ by {diff/sr_m:.2f}s, "+\
            f"which is more than the current threshold ({THRESHOLD_DIFF_SECONDS} s)\n\n"+\
            "Skipping this pair.\n\n"
        )
        continue
    
    # Split differences, contracting longer audio and dilating shorter audio
    scale_audio(
        input_file=audio_m,
        output_file=audio_m,
        delta_frames=-diff//2 if diff >=0 else diff//2
    )
    scale_audio(
        input_file=audio_f,
        output_file=audio_f,
        delta_frames=diff//2 if diff >=0 else -diff//2
    )
    
    # Combine to stereo and rescale to relative dB
    combine_audio_stereo(
        audio_left=audio_f,
        audio_right=audio_m,
        output_file=OUTPUT_DIR / f'{stereo_name1}_no_probe.wav'
    )
    scale_audio_to_relative_db(
        audio_to_scale_path=OUTPUT_DIR / f'{stereo_name1}_no_probe.wav',
        reference_audio_path=attention_probe_path,
        target_db_diff=-ABSOLUTE_RELATIVE_ATTENUATION_DB # dB
    )
    combine_audio_stereo(
        audio_left=audio_m,
        audio_right=audio_f,
        output_file=OUTPUT_DIR / f'{stereo_name2}_no_probe.wav'
    )
    scale_audio_to_relative_db(
        audio_to_scale_path=OUTPUT_DIR / f'{stereo_name2}_no_probe.wav',
        reference_audio_path=attention_probe_path,
        target_db_diff=-ABSOLUTE_RELATIVE_ATTENUATION_DB # dB
    )
    
    # Add attention tracks
    sr_data, data1 = read_wav(OUTPUT_DIR / f'{stereo_name1}_no_probe.wav', return_sample_rate=True)
    sr_data, data2 = read_wav(OUTPUT_DIR / f'{stereo_name2}_no_probe.wav', return_sample_rate=True)
    normalized_data1 = data1 / np.max(np.abs(data1))
    normalized_data2 = data2 / np.max(np.abs(data2))
    n_probes1, track_left1, track_right1 = create_attention_track(
        duration_samples=len(data1),
        sr=COMMON_SAMPLE_RATE,
        probe_audio_path=attention_probe_path
    )
    n_probes2, track_left2, track_right2 = create_attention_track(
        duration_samples=len(data2),
        sr=COMMON_SAMPLE_RATE,
        probe_audio_path=attention_probe_path
    )
    print(f'Added {n_probes1} probes to {stereo_name1}, and {n_probes2} probes to {stereo_name2}')
    normalized_data1[:,0] += track_left1
    normalized_data2[:,0] += track_left2
    normalized_data1[:,1] += track_right1
    normalized_data2[:,1] += track_right2
    if SCRAMBLED_PROBE:
        save_wav(OUTPUT_DIR / f'{stereo_name1}_scrambled.wav', sr_data, normalized_data1)
        save_wav(OUTPUT_DIR / f'{stereo_name2}_scrambled.wav', sr_data, normalized_data2)
    else:
        save_wav(OUTPUT_DIR / f'{stereo_name1}_not_scrambled.wav', sr_data, normalized_data1)
        save_wav(OUTPUT_DIR / f'{stereo_name2}_not_scrambled.wav', sr_data, normalized_data2)
    
    # TODO hacer el psyexp:
    # 1a version: instrucciones dependientes del audio (.csv con paths e instruccion asociada a c/u). El audio tal cual e incluir preguntas de compresion --> preguntar si las tienen armadas
    # ---> meter ttls al principio y final del audio para verificar temporalidad. Si funciona descartar version2
    
    # ---> podemos dejar un punto de fijación. Se indica genero de la voz y oreja, intercalar al final preguntas de compresión (son orales, entonces dejar el espacio o un indicador)
    
    # Termina la historia, pregunta escrita y abajo diga decile al experimentador tu respuesta  y que el diga apreta la barra para seguir.
    
    
    
    # 2a version: audios sin tonos y en stereo, mandar en paralelo los bips con ttl (el cuando se puede meter en el .csv)