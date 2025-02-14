#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import streamlit as st
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave
import pyaudio

# Function to list available audio devices
def list_audio_devices():
    devices = sd.query_devices()
    st.write("Available Audio Devices:", devices)

# Function to record audio
def record_audio(duration=5, samplerate=44100):
    try:
        # Get default input device
        default_device = sd.query_devices(kind='input')
        st.write(f"Using Input Device: {default_device['name']} (Index: {default_device['index']})")

        # Set the default device before recording
        sd.default.device = default_device['index']

        st.info("Recording... Speak now!")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()
        
        # Save the recorded audio to a temporary file
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with wave.open(temp_audio_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(recording.tobytes())

        return temp_audio_path

    except Exception as e:
        st.error(f"Error recording audio: {e}")
        return None

# Function to transcribe audio
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Streamlit UI
st.set_page_config(page_title="Echo_Script", page_icon="🎙️", layout="centered")
st.title("🎙️ Echo_Script")
st.markdown("Record your voice or upload an audio file to get the transcription.")

# List available devices
list_audio_devices()

# Record button
if st.button("🎤 Record Voice (5s)"):
    audio_path = record_audio()
    
    if audio_path:
        st.audio(audio_path, format="audio/wav")
        
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(audio_path)
        
        st.subheader("📝 Transcription:")
        st.write(transcription)
        os.remove(audio_path)

# File uploader
uploaded_file = st.file_uploader("Or upload an audio file", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name
    
    st.audio(uploaded_file, format="audio/wav")
    
    if st.button("Transcribe Uploaded Audio"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(temp_audio_path)
        
        st.subheader("📝 Transcription:")
        st.write(transcription)
        os.remove(temp_audio_path)


