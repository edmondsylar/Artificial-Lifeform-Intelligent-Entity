import io
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# get key from .env file
key = os.getenv("OPENAI_API_KEY")


os.environ["OPENAI_API_KEY"] = key

client = OpenAI()
openai.api_key = key
client = OpenAI(api_key=key)


def stream_and_play(text):
  response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx", #nova, fable, echo, alloy, shimmer
    input=text,
  )

  # Convert the binary response content to a byte stream
  byte_stream = io.BytesIO(response.content)

  # Read the audio data from the byte stream
  audio = AudioSegment.from_file(byte_stream, format="mp3")

  # Play the audio
  play(audio)
