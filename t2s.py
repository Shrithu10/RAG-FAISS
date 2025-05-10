import io
from google.cloud import texttospeech, speech
from google.oauth2 import service_account

def synthesize_text(text, credentials_file, language_code, voice_name, speaking_rate, output_path):
    credentials = service_account.Credentials.from_service_account_info(credentials_file)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)

def transcribe_audio(audio_path, credentials_file, language_code):
    credentials = service_account.Credentials.from_service_account_info(credentials_file)
    client = speech.SpeechClient(credentials=credentials)
    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)
    transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    return transcript
