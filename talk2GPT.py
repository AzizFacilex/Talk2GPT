import pyaudio
import wave
import audioop
import math
import openai
import pygame
from google.cloud import texttospeech
import time
import os

audio = pyaudio.PyAudio()

CHUNK = 1024  # number of audio frames per buffer
FORMAT = pyaudio.paInt16  # audio format (16-bit signed integer)
CHANNELS = 1  # number of audio channels (mono)
RATE = 16000  # sample rate (Hz)
THRESHOLD = 50  # audio level threshold for detecting speech
SILENCE_LIMIT = 2  # seconds of silence needed to stop recording

frames = []
recording = False
silence_counter = 0
client = texttospeech.TextToSpeechClient()
openai.api_key = os.getenv('openai_key')
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16)

while True:
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)
    decibel = 20 * math.log10(rms)

    if decibel > THRESHOLD:
        if not recording:
            print("Recording started")
            recording = True
        frames.append(data)
        silence_counter = 0
    else:
        if recording:
            silence_counter += 1

        if silence_counter > SILENCE_LIMIT * (RATE / CHUNK):
            if recording:
                print("Recording stopped")
                recording = False
                if len(frames) < 5:
                    continue
                filename = "recorded_audio.wav"
                start_time = time.time()
                with wave.open(filename, "wb") as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(audio.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b"".join(frames))
                end_time = time.time()
                print("Execution time:", end_time - start_time, "seconds")
                frames = []
                with open("recorded_audio.wav", "rb") as audio_file:
                    result = openai.Audio.transcribe(
                        "whisper-1", audio_file)['text']
                print(result)
                responsegpt = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                            "content": "You are a tourist guide. answer shortly"},
                        {"role": "user", "content": result}
                    ]
                )
                synthesis_input = texttospeech.SynthesisInput(
                    text=responsegpt['choices'][0]['message']['content'])
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )

                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config)
                with open('output2.wav', 'wb') as out:
                    out.write(response.audio_content)

                pygame.mixer.init()
                pygame.mixer.music.load("output2.wav")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                silence_counter = 0
                time.sleep(2)
