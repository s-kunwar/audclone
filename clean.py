import noisereduce as nr
import numpy as np
from pydub import AudioSegment
import os

def clean_audio(input_file, output_file):
    print(f"--- Processing: {input_file} ---")
    
    # 1. Load the audio using Pydub (handles .m4a, .mp3, etc.)
    audio = AudioSegment.from_file(input_file)
    
    # Convert to Mono and set a standard frame rate for the model
    audio = audio.set_channels(1).set_frame_rate(22050)
    
    # 2. Convert Pydub audio to a Numpy array for noise reduction
    samples = np.array(audio.get_array_of_samples())
    rate = audio.frame_rate
    
    print("Step 1: Reducing background noise...")
    # 3. Perform Noise Reduction
    # stationary=True is great for removing laptop fan noise (perfect for your i7!)
    reduced_noise = nr.reduce_noise(y=samples, sr=rate, stationary=True, prop_decrease=0.8)

    # 4. Convert back to Pydub AudioSegment
    cleaned_audio = AudioSegment(
        reduced_noise.astype(np.int16).tobytes(), 
        frame_rate=rate,
        sample_width=2, # 16-bit
        channels=1
    )

    print("Step 2: Normalizing and trimming...")
    # Normalize volume (so the AI doesn't have to "strain" to hear you)
    normalized_audio = cleaned_audio.normalize()
    
    # Strip silence
    final_audio = normalized_audio.strip_silence(silence_thresh=-45, padding=100)

    # 5. Export as WAV (which XTTS v2 requires)
    final_audio.export(output_file, format="wav")
    
    print(f"✅ Success! Cleaned file saved as: {output_file}")

# Usage
# Make sure the filename matches your file: "audiio.m4a"
clean_audio("vp.m4a", "ac.wav")