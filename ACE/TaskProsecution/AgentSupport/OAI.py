# function calling open aa api 
from openai import OpenAI
import requests
import os


class OAISupport:
    def __init__(self, key):
        self.key = key
        self.client = OpenAI(api_key=self.key)

    def chat(self, conversation):
        # set the model to use.
        model = 'gpt-3.5-turbo-1106'
        response = self.client.chat.completions.create(
            model=model,
            messages=conversation,
        )

        # get the response.
        res = response.choices[0].message.content.strip()

        # return the response.
        return res