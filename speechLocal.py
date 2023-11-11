from vosk import Model, KaldiRecognizer
import sys
import pyaudio

model = Model(r"D:\PTYPED\Research\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(2000)
    # if length(data) == 0:
    #     break
    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())
    else:
        print(recognizer.PartialResult())