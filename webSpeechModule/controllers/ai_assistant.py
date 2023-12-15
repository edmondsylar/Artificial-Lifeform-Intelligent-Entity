import google.generativeai as palm
import os 
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("google_palm_api_key")

palm.configure(api_key=google_api_key)

defaults = {
  'model': 'models/chat-bison-001',
  'temperature': 0.9,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
}
context = "You are Alfie, a  useful research assistant. You are helping a researcher with their research and normal queries."
examples = []


def chat(conversation_history):

    response = palm.chat(
    **defaults,
    context=context,
    examples=examples,
    messages=conversation_history
    )
    print(response.last) # Response of the AI to your most recent request

    return response.last