import streamlit as st
import os
import json
from pathlib import Path
from t2s import synthesize_text, transcribe_audio

MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)

# ---- CREDENTIALS ----
st.sidebar.header("Google Cloud Credentials")
credentials_json = st.sidebar.text_area(
    "Paste your Google Cloud service account JSON here (as plain text):",
    height=200
)
credentials_file = None
if credentials_json:
    try:
        credentials_file = json.loads(credentials_json)
        st.sidebar.success("Credentials loaded.")
    except Exception as e:
        st.sidebar.error(f"Invalid JSON: {e}")

st.title("Google Cloud Text-to-Speech & Speech-to-Text")

# ---- TEXT TO SPEECH SECTION ----
st.header("Text to Speech")
text = st.text_area("Enter text to synthesize:")
language_code = st.text_input("Language code", value="en-US")
voice_name = st.text_input("Voice name", value="en-US-Wavenet-D")
speaking_rate = st.slider("Speaking rate", min_value=0.25, max_value=4.0, value=1.0, step=0.05)
tts_button = st.button("Synthesize Speech")

if tts_button and credentials_file and text.strip():
    output_path = MEDIA_DIR / "output.wav"
    try:
        synthesize_text(text, credentials_file, language_code, voice_name, speaking_rate, str(output_path))
        st.audio(str(output_path), format="audio/wav")
        st.success("Speech synthesized successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

# ---- SPEECH TO TEXT SECTION ----
st.header("Speech to Text")
audio_file = st.file_uploader("Upload a WAV file (mono, 16kHz)", type=["wav"])
st.caption("For best results, upload a mono WAV file sampled at 16kHz.")
stt_language_code = st.text_input("Language code for transcription", value="en-US", key="stt_lang")
stt_button = st.button("Transcribe Audio")

if stt_button and credentials_file and audio_file:
    audio_path = MEDIA_DIR / "uploaded_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())
    try:
        transcript = transcribe_audio(str(audio_path), credentials_file, stt_language_code)
        st.write("**Transcription:**")
        st.success(transcript)
    except Exception as e:
        st.error(f"Error: {e}")
