import speech_recognition as sr
from pydub import AudioSegment
import os

from pydub import AudioSegment
import speech_recognition as sr
import os

def transcribe_audio_file(mp3_path: str, language: str = "en-US") -> str:
    wav_path = mp3_path.replace(".mp3", ".wav")

    try:
        # Convert mp3 to wav
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")

        # Transcribe using Google Web Speech API
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)

        return text

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

