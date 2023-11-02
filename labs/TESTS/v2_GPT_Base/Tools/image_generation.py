import threading
import time
import os
import openai
from data import working_memory
from SystemModules.memory_management import _build_memory

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt):
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return {
        'task': f'generate an image based on the following prompt: \n{prompt}',
        'Status': 'Complete',
        'content': image_url
    }

    _build_memory(working_memory, 'system', f'completed generating the picture, Find the url attached. URL: {image_url}')

# print(generate_image('hyper-realistic picture of a cat wearing a space suit, HD, fantasy, cinematic lighting'))