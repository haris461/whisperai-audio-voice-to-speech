import sounddevice as sd

# Set the correct microphone index
sd.default.device = 5 #  Change this to your correct mic index

print(f"Microphone set to device index: {sd.default.device}")
