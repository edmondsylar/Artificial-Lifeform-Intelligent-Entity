import google.generativeai as palm
import os
import requests

class PalmSupport:
    def __init__(self, api_key, constitution):
        self.api_key = api_key
        self.constitution = constitution

        palm.configure(api_key=self.api_key)
        self.defaults = {
            'model': 'models/chat-bison-001',
            'temperature': 0.9,
            'candidate_count': 1,
            'top_k': 40,
            'top_p': 0.95,
        }

    # this function take in the examples and messages and returns the response.
    def chat(self, examples=[], messages=[]):

        response = palm.chat(
            **self.defaults,
            context=self.constitution,
            examples=examples,
            messages=messages
        )

        return response.last

    def instruct(self, instruction, task):
        

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

        prompt = f"""
        {instruction}


        {task}
        
        output:"""

        response = palm.generate_text(
            **defaults,
            prompt=prompt
        )

        return response.result
    