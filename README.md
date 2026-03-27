# Speech Cloning Project

## Overview

This repository contains a local speech cloning and text-to-speech workflow for Windows using `TTS`, `torch`, and audio processing libraries. It includes:

- `chat.py`: interactive streaming text-to-speech from typed input
- `clean.py`: audio cleanup/denoise pipeline for source playback sample
- `test.py`: direct TTS generation to file via model API
- `requirements.txt`: exact package dependencies

The code is configured for a local model path and is designed to run on CPU (and optionally CUDA with small edits). It uses a TorchCodec workaround for `torchaudio` to handle audio file loading reliably with `soundfile` fallback.

---

## Prerequisites

1. Python 3.10+ (3.11 recommended)
2. A virtualenv or conda environment in project folder
3. Windows 10/11 (tested)
4. Git repository initialized in `C:\Suraj\code\python\clone`

---

## Setup

1. Activate virtual environment:

   ```powershell
   cd C:\Suraj\code\python\clone
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Confirm model files exist at the path configured in `chat.py` (default):

   `C:\Users\suraj\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2`

   If not available, change `--model-path` in `chat.py` or update the path manually.

---

## `requirements.txt`

The project uses:

- `torch`
- `numpy`
- `torchaudio`
- `soundfile`
- `sounddevice`
- `TTS`
- `noisereduce`
- `pydub`

---

## Usage

### 1) `clean.py` (audio cleanup)

Clean a source file and output `ac.wav` by default:

```powershell
python clean.py input_file.m4a output_file.wav
```

Example:

```powershell
python clean.py vp.m4a ac.wav
```

After success, `ac.wav` is available for TTS speaker conditioning.

### 2) `test.py` (TTS generation to file)

Generate a TTS sample and save to a file:

```powershell
python test.py --text "Hello from CLI" --speaker-wav ac.wav --language hi --output final_clone_output.wav
```

Parameters:

- `--text`: required text to synthesize
- `--speaker-wav`: path to cleaned sample (default `ac.wav`)
- `--language`: language code (`hi`, `en`, etc.)
- `--output`: destination file

### 3) `chat.py` (interactive streaming TTS)

Interactive mode (default):

```powershell
python chat.py
```

One-shot text mode:

```powershell
python chat.py --text "Hello from chat mode" --lang en
```

Command-line options:

- `--model-path`: path to the local model folder
- `--text`: text to speak immediately
- `--lang`: `auto`, `en`, or `hi` for one-shot mode

---

## Git Instructions

1. Initialize repository (already done):

```powershell
git init
```

2. Add `.gitignore` suggested entries:

```gitignore
__pycache__/
*.pyc
venv/
*.wav
*.m4a
*.pth
*.pt
```

3. Stage and commit:

```powershell
git add .
git commit -m "Initial project setup with CLI support and requirements"
```

4. Push to remote (if configured):

```powershell
git push -u origin main
```

---

## Notes & Troubleshooting

- If `soundfile` errors occur:

  ```powershell
  pip install soundfile
  ```

- If `torchaudio` TorchCodec errors occur, the fallback path via `soundfile` is built into scripts.

- If your GPU is available, set `--device cuda` for faster synthesis, but ensure PyTorch with CUDA is installed.

- For Hindi auto-detect in `chat.py`, it checks Unicode Devanagari range.

---

## Conventions

- `ac.wav`: cleaned speaker audio sample input for TTS voice adaptation
- `vp.m4a`: unprocessed raw voice file to process
- Runtime assets `2.wav`, `3.wav` produced locally by tests (do not commit)

---
