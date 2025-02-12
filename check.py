import sounddevice as sd
import numpy as np

fs = 44100  # Sample rate
duration = 5 # Record for 3 seconds

print("Recording...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
sd.wait()
print("Recording complete.")

# Play the recorded audio
print("Playing back...")
sd.play(audio, samplerate=fs)
sd.wait()
print("Playback complete.")
