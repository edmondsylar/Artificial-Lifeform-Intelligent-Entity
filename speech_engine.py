from vosk import Model, KaldiRecognizer
import sys
import pyaudio
import threading
from functions.speech2text import _interact
import json
from rich.console import Console

console = Console()

model = Model(r"E:\Code PTYPED\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


# speech recognition engine start
def start_speech_recognition():
    print("Alfie Speech Recognizer Started.")
    while True:
        data = stream.read(4096)
        if len(data) == 0:
            print("No data received.")
            continue
        if recognizer.AcceptWaveform(data):
            
            # jsonified response
            response = json.loads(recognizer.Result())
            speech_text = response["text"]
            print("You: ", speech_text)

            if "hey buddy" in speech_text or "alfie" in speech_text:
                print("Callling Alfie: ", speech_text)
                threading.Thread(target=_interact, args=(speech_text,)).start()


