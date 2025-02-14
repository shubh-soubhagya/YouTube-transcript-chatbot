import speech_recognition as sr
from pydub import AudioSegment

# Convert MP3 to WAV
audio = r"C:\Users\hp\Desktop\ytpro\audio.mp3"
sound = AudioSegment.from_mp3(audio)
sound.export("audio.wav", format="wav")

# Recognize Speech from WAV
recognizer = sr.Recognizer()
with sr.AudioFile("audio.wav") as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)
    print("Recognized Text:", text)
