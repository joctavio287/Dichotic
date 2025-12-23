# Dichotic

Preprocess audiobook audio files for a dichotic listening experiment.

The main entrypoint is `split_audios.py`, which:

- Converts paired MP3s (male/female narration) to WAV
- Normalizes durations within a pair (simple time-stretch by interpolation)
- Builds stereo dichotic stimuli (female-left/male-right and female-right/male-left)
- Optionally injects randomized “attention probes” (either TTS syllable or a tone)
- Exports PsychoPy-ready CSV tables pointing at the generated WAV files

## What you get

After running, you will have:

- `data/processed_audios/no_probe/*.wav` (stereo files without probes)
- `data/processed_audios/with_probe/*.wav` (stereo files with probes added)
- `data/processed_audios/attention_probe.wav` (the probe sound)
- `data/attention_probe_<TYPE>_<DURATION_MS>_profile.png` (probe profile plot)
- `psychopy_experiment/audiobook_combinations_no_probes.csv`
- `psychopy_experiment/audiobook_combinations_probes.csv`

## Folder structure

- `data/original_audios/`: input MP3 files
- `data/intermediate_audios/`: temporary WAVs created during processing (deleted at the end)
- `data/processed_audios/`: outputs
	- `no_probe/`: stereo WAVs without probes
	- `with_probe/`: stereo WAVs with probes
- `psychopy_experiment/`: PsychoPy experiment and the generated CSV condition files

## Input requirements (IMPORTANT)

`split_audios.py` expects **paired** male/female versions of the same stories.

### Naming convention

The code relies on underscores in filenames. Use this pattern:

`<NN>_<STORY>_mujer.mp3`
`<NN>_<STORY>_hombre.mp3`

Where:

- `<NN>` is a number (used for ordering), e.g. `01`, `02`, …
- `<STORY>` is the story identifier (must NOT contain `_` underscores)
- The filename must contain either the substring `mujer` or `hombre`

Examples:

- `01_caperucita_mujer.mp3`
- `01_caperucita_hombre.mp3`

### Pairing rules enforced by the script

- The total number of MP3 files must be even.
- For each `<STORY>`, there must be a matching male and female file.
- Male and female story names must match exactly (based on the second underscore-separated token).

If these do not hold, the script will `assert` and stop.

## Processing specification

### 1) Pairing and combinations

The script orders all female files by `<NN>` and all male files by `<NN>`, then creates combinations in a consecutive pattern:

- If `i` is even, it combines `female[i]` with `male[i+1]`, and `female[i+1]` with `male[i]`.

For each pair it creates **two stereo conditions**:

- `..._FL_MR_...`: female in left, male in right
- `..._FR_ML_...`: female in right, male in left

### 2) Conversion to WAV

Each MP3 is converted to WAV into `data/intermediate_audios/`.

Conversion is done via `ffmpeg` (through `ffmpeg-python`).

### 3) Sample rate validation

The script asserts that the male and female WAVs for a combination have the same sample rate.

### 4) Duration matching

The script measures the sample-length difference between the two WAVs.

- If the absolute mismatch exceeds `THRESHOLD_DIFF_SECONDS`, the pair is skipped.
- Otherwise it “splits” the difference and time-stretches each side so they meet in the middle.

Implementation note: `utils/audio_helpers.scale_audio()` uses 1D interpolation to resample to the target frame count.

### 5) Building stereo WAVs (no-probe)

The script exports stereo WAVs to `data/processed_audios/no_probe/`.

It then scales each stimulus to be `ABSOLUTE_RELATIVE_ATTENUATION_DB` dB below the probe reference, using energy-based scaling with clipping protection.

### 6) Probe generation

An attention probe WAV is created at `data/processed_audios/attention_probe.wav`.

Probe types:

- If `PROBE_TYPE` is a **string** (e.g. `"va"`), the probe is synthesized via `gTTS` (Spanish locale) and trimmed to `PROBE_DURATION`.
- If `PROBE_TYPE` is an **int**, it generates a tone (currently implemented as 1000 Hz in `audio_helpers.py`).

The script also generates a diagnostic plot:

- `data/attention_probe_<TYPE>_<DURATION_MS>_profile.png`

If `SCRAMBLED_PROBE=True` and `PROBE_TYPE` is a string, the probe audio can be segmented and shuffled.

### 7) Probe placement and mixing (with-probe)

For each no-probe stereo file, the script generates an attention track:

- Random probe placement after an initial delay
- Random ISIs sampled from `[0.2, 0.5, 1.0]` seconds
- Equal number of probes on left and right channels

It then adds the track to the stereo stimulus and saves to `data/processed_audios/with_probe/`.

### 8) PsychoPy CSV tables

Two CSVs are written under `psychopy_experiment/`:

- `audiobook_combinations_no_probes.csv`
- `audiobook_combinations_probes.csv`

Each row contains:

- `filename`: relative path (prefixed with `..`) to the WAV file
- `condition_label`: derived from the filename tokens (e.g. `FL_MR_AB`)
- `number_story_A`, `number_story_B`: extracted from the filename

## Configuration (edit in split_audios.py)

Key parameters at the top of `split_audios.py`:

- `ABSOLUTE_RELATIVE_ATTENUATION_DB`: dB difference between stimuli and probe
- `NUMBER_OF_SCRAMBLE_SEGMENTS`: scrambling granularity (if enabled)
- `THRESHOLD_DIFF_SECONDS`: skip threshold for duration mismatch
- `COMMON_SAMPLE_RATE`: target sample rate for probe generation
- `PROBE_DURATION`: probe duration in seconds
- `ATTACK_THRESHOLD`: probe attack detection threshold for profiling
- `PROBE_TYPE`: probe stimulus (string TTS or int tone)
- `SCRAMBLED_PROBE`: whether to scramble TTS probes

## Notes about PsychoPy

The preprocessing pipeline does not require PsychoPy. For that another environment is suggested (python 3.10, psyhcopy 2025.2.3).
The `psychopy_experiment/` folder contains the experiment files and expects the generated CSVs + WAVs.
