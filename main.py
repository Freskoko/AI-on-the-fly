import openai
import os
from dotenv import load_dotenv
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import io
import keyboard
import threading
import time

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")
openai.api_key = apikey

def ask_question(question):

    response = openai.ChatCompletion.create(
        model="gpt-4", #model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that answers a question, in a consice and to the point matter"},
            {"role": "user", "content": f"Generate an answer to the question: {question} answer in one or two sentences, make it interesting!"}
        ],
        temperature=0.95,
        max_tokens=50,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
        
    return response.choices[0]["message"]["content"]


def transcribe_audio_from_user():
    with open("user_output.wav", "rb") as audio_file:
        response = openai.Audio.transcribe(file=audio_file, model="whisper-1")
    return response


def record_audio(filename, rate=48000, channels=2, chunk=1024, format=pyaudio.paInt16):
    audio = pyaudio.PyAudio()

    # Open a streaming stream
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    print("Press and hold the 'r' key to start recording...")

    # Wait for the 'b' key to be pressed
    keyboard.wait('r')

    print("Recording...")

    frames = []

    # Record audio while the 'b' key is being held down
    while keyboard.is_pressed('r'):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as aWAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))


def TextToSpeech(text, output_file, lang="en"):
    tts = gTTS(text=text, lang=lang)
    with io.BytesIO() as audio_file:
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        audio = AudioSegment.from_file(audio_file, format="mp3")
        play(audio)
    return "Saved"



def record_and_process_audio():
    record_audio("user_output.wav")
    user_inp = (transcribe_audio_from_user())
    print(user_inp)
    from_bot = (ask_question(user_inp))
    output_file = "bot_output.mp3"
    TextToSpeech(from_bot, output_file)
    exit()

record_and_process_audio()