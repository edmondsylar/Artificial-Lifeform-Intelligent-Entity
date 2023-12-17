from pathlib import Path
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
import time
from datetime import datetime

images = [] # list of images
perceptions = [] # list of perceptions from the model

# load .env file
load_dotenv()

# gemini api key
genai.configure(api_key=os.getenv('google_gemini_api_key'))

# Set up the model
generation_config = {
  "temperature": 0.4,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]

model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings
    )

def delete_images(image_urls):
  for image_url in image_urls:
    if os.path.isfile(image_url):
      os.remove(image_url)
    else:
      print(f"Error: {image_url} not a valid filename")


# generate insights function 
def generate_insights(images, prompt):
    # Set up the model
    # ... (same as before)

    # Validate that images are present
    for img in images:
        if not Path(img).exists():
            raise FileNotFoundError(f"Could not find image: {img}")

    # Read image data
    image_parts = [{"mime_type": "image/jpeg", "data": Path(img).read_bytes()} for img in images]

    # Create prompt parts
    prompt_parts = [prompt] + image_parts

    # Generate and return response
    response = model.generate_content(prompt_parts)
    return response.text

# absolute path to this file
ablsolute_path = Path(__file__).parent.absolute()

# list of the images


# get all the images
for image in os.listdir(os.path.join(ablsolute_path, 'images')):
    images.append(os.path.join(ablsolute_path, 'images', image))


print (images)



# we are going to send one image at a time with a 2 sencod delay between each image
# this is to simulate a real world use case
for img in images[]: #last 10 images
    prompt = f"""
    #Grounding Instruction.
    You are the eyes of a system that is trying to understand the world. you receive images every 2 seconds and just respond with imporatnt insights about the image. for the sysystem to properly understand what it needs, you also receive your previous outputs to help you better understand the concept of motion.

    #previous outputs
    {perceptions}

    # Note: These can be empty if the system has just started.

    Current Time: {datetime.now().strftime("%H:%M:%S")}
    """


    response = generate_insights([img], prompt)
    print(response, "\n\n")
    perceptions.append(str(response))

    time.sleep(2)


