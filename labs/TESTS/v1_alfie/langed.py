from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm
from langchain.chat_models import ChatGooglePalm

import google.generativeai
import os

google_api_key="AIzaSyDn2fvOXSrPnm7hxCYQKwClE93hWfk8ch0"

llm = GooglePalm(google_api_key=google_api_key)
llm.temperature = 0.1

prompts = ['Explain the difference between effective and affective with examples']
llm_result = llm._generate(prompts)

print(llm_result.generations[0][0].text)