import os
import torch
import functools
import sounddevice as sd
import numpy as np
import torchaudio
import soundfile as sf

torch.set_num_threads(8)

# --- 1. THE ULTIMATE BYPASS (Fixes the TorchCodec error everywhere) ---
def manual_load(uri, *args, **kwargs):
    try:
        # Try standard loading
        return torchaudio.load_orig(uri, *args, **kwargs)
    except Exception:
        # Fallback to soundfile if TorchCodec/FFmpeg fails
        data, samplerate = sf.read(uri, dtype='float32', always_2d=True)
        return torch.from_numpy(data.T), samplerate

if not hasattr(torchaudio, 'load_orig'):
    torchaudio.load_orig = torchaudio.load
    torchaudio.load = manual_load

# Master Key for PyTorch 2.6 security
torch.load = functools.partial(torch.load, weights_only=False)
os.environ["TORCHAUDIO_USE_TORCHCODEC"] = "0"
# -----------------------------------------------------------------------

from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

# Optimization for i7-13th Gen
device = "cpu"
torch.set_num_threads(12) 

print("--- 🚀 Loading Streaming Engine ---")
# Adjust these paths if your username isn't 'suraj'
model_path = r"C:\Users\suraj\AppData\Local\tts\tts_models--multilingual--multi-dataset--xtts_v2"

config = XttsConfig()
config.load_json(os.path.join(model_path, "config.json"))
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir=model_path, eval=True)
model.to(device)

print("--- 🎙️ Analyzing your voice sample ---")
# Now this will use our manual_load bypass!
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["ac.wav"])

def stream_speech(text, lang="en"):
    print(f"--- ⚡ Speaking: {text[:30]}... ---")
    
    # Increase latency to 'high' and adjust blocksize to prevent crackling
    # samplerate must be 24000 for XTTS v2
    with sd.OutputStream(samplerate=24000, channels=1, dtype='float32', blocksize=2048) as stream:
        for chunk in model.inference_stream(
            text, 
            lang, 
            gpt_cond_latent, 
            speaker_embedding,
            stream_chunk_size=30,  # 🚀 INCREASED from 20 to 60 for smoothness
            overlap_chunk_size=10, # 🚀 Adds a 'blend' between chunks
            temperature=0.80
        ):
            # Ensure the chunk is a numpy array and push to speakers
            chunk_np = chunk.cpu().numpy()
            stream.write(chunk_np)

# --- 🎤 INTERACTIVE CHAT MODE ---
print("\n✅ System Ready! Type something in English or Hindi.On Day 2 in Tokyo, I explored its spiritual and modern sides, visiting Senso-ji Temple, the Imperial Palace, and the Chiyoda area, ending with a walk through Shibuya Crossing.")
while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ['q', 'exit', 'quit']: break
    
    # Simple check for Hindi characters to switch language automatically
    lang = "hi" if any("\u0900" <= c <= "\u097F" for c in user_input) else "en"
    stream_speech(user_input, lang=lang)