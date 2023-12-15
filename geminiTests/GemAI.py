# this is going to have temporary memory using a simple list.
import google.generativeai as genai
from gtts import gTTS
import threading

import pyaudio
from io import BytesIO
import threading

def play_audio(audio_data):
    print("playing audio: Called with Audio Data")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def text_to_audio(text):
    print("converting text to audio")
    audio_fp = BytesIO()
    tts = gTTS(text=text, lang='en')
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    play_audio(audio_fp.read())


genai.configure(api_key="AIzaSyCtGFwP8vcxz_qWlqU932IP_s7AsAghpvw")

# Set up the model
model = genai.GenerativeModel(model_name="gemini-pro")
  

# Start a conversation
convo = model.start_chat()

while True:
    msg = input("You: ")
    # Send a message

    msg = fr'''
    {msg}

    # instructions.
    You are Alfie (ALFIE - Artificial Lifeform Intelligent Entity) an AGI System that is being built to understand and interact with humans. all the responses.
    you are giving are going to be in the form of speech not necessarily text so you will need to ensure your responses are in the form of speech because the system is going to convert them to speech.

    Note: please don't introduce yourself unless you are asked to do so, the 'instructions' are just for you to ground your responses and interactions.

    '''
    convo.send_message(msg)
    # Get the response
    print(convo.last.text)

    def play_response_audio(response):
        print("playing response audio")
        threading.Thread(target=text_to_audio, args=(response,)).start()

    play_response_audio(convo.last.text)
    # print("\n\\n")
