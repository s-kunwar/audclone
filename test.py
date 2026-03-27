import os
import torch
import functools
import soundfile as sf # We use this as the backup loader

# 1. Master Key for PyTorch 2.6 security
torch.load = functools.partial(torch.load, weights_only=False)

from TTS.api import TTS
import time

# 2. THE ULTIMATE BYPASS: Manually patch the loading error
import torchaudio
def manual_load(uri, *args, **kwargs):
    try:
        # Try the normal way first
        return torchaudio.load_orig(uri, *args, **kwargs)
    except Exception:
        # Fallback to soundfile (The "TorchCodec is missing" fix)
        data, samplerate = sf.read(uri, dtype='float32', always_2d=True)
        # Convert to the [channels, time] format XTTS expects
        return torch.from_numpy(data.T), samplerate

if not hasattr(torchaudio, 'load_orig'):
    torchaudio.load_orig = torchaudio.load
    torchaudio.load = manual_load

# CPU Optimization
device = "cpu"
torch.set_num_threads(12) 

print("--- 🚀 Initializing XTTS v2 ---")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    
    print("--- 🎙️ Generating Audio ---")
    start_time = time.time()

    # ... (Keep your existing imports and patches at the top) ...

    tts.tts_to_file(

        text="Keep your existing imports and patches at the top, and then add this function call to generate the audio file. You can adjust the parameters as needed.",
        speaker_wav="ac.wav", # Your English sample works fine here!
        language="hi",

        # --- 🎭 THE HUMANIZER SETTINGS ---
        temperature=0.9,      # Higher = more emotional/varying (0.7 is standard, 0.8 is wild)
        speed=1.0,            # 1.0 is normal. Try 0.9 for a more relaxed, natural pace.
        length_penalty=1.0,    # Controls how long the sentences are
        repetition_penalty=5.0, # Prevents the AI from getting stuck on a sound
        top_k=50,              # Limits the vocabulary to the most likely next sounds
        top_p=0.85,            # Adds "richness" to the tone
        # ---------------------------------
    )

    print(f"--- ✅ SUCCESS! ---")
    print(f"File: {os.path.abspath('final_clone_output.wav')}")

except Exception as e:
    print(f"❌ Final Boss Error: {e}")
    print("\n💡 Tip: If you see 'soundfile' missing, run: pip install soundfile")