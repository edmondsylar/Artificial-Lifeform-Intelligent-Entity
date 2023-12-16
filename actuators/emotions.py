
import google.generativeai as genai
import os 
from dotenv import load_dotenv

load_dotenv()

# get the api key from the .env file.
api_key = os.getenv('google_gemini_api_key')

genai.configure(api_key=api_key)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":"BLOCK_LOW_AND_ABOVE"},{"category":"HARM_CATEGORY_TOXICITY","threshold":"BLOCK_LOW_AND_ABOVE"},{"category":"HARM_CATEGORY_VIOLENCE","threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_SEXUAL","threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_MEDICAL","threshold":"BLOCK_MEDIUM_AND_ABOVE"},{"category":"HARM_CATEGORY_DANGEROUS","threshold":"BLOCK_MEDIUM_AND_ABOVE"}],
}


def generate_emotion(input):

    prompt = fr"""
    You are a human reaction mimic module for a huge Autonomous AGI System by perfectly following the instructions.

    you are given; 
    1. The conversation history (summarize the key points), 
    2. The user's emotional state (indicate the emotional state), 
    3. And the purpose of the conversation (state the purpose), 
    
    instruction: 
    generate a text-based description of the perfect emoji or picture (text-to-image prompt) to best suite the AGI system's response to the user's latest input, accurately mimicking the AGI's inner "emotional-like" expression based on the information provided as below:

    input: 
    {input}
    
    """


    response = genai.generate_text(
    **defaults,
    prompt=prompt
    )

    print(response.result)