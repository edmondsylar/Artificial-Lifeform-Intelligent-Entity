import os
import time
from pathlib import Path
import google.generativeai as genai
from datetime import datetime

genai.configure(api_key='')

class VisionEngine:
  def __init__(self):
    self.generation_config = {
      "temperature": 0.4,
      "top_p": 1,
      "top_k": 32,
      "max_output_tokens": 4096,
    }

    self.safety_settings = [
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

    self.model = genai.GenerativeModel(
      model_name="gemini-pro-vision",
      generation_config=self.generation_config,
      safety_settings=self.safety_settings
    )

    self.perceptions = []
    self.images = []
    self.ablsolute_path = Path(__file__).parent.absolute()

  def delete_images(self, image_urls):
    for image_url in image_urls:
      if os.path.isfile(image_url):
        os.remove(image_url)
      else:
        print(f"Error: {image_url} not a valid filename")

  def generate_insights(self, images, prompt):
    print(fr'received {len(images)} images and processing... \n\nPrevious Perceptions: {self.perceptions}')

    for img in images:
      if not Path(img).exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    image_parts = [{"mime_type": "image/jpeg", "data": Path(img).read_bytes()} for img in images]
    prompt_parts = [prompt] + image_parts
    response = self.model.generate_content(prompt_parts)
    return response.text

  def insights_loop(self):
    try:
      last_5_perceptions = self.perceptions[-5:]
    except:
      last_5_perceptions = []

    while True:
      print('running...')
      time.sleep(1.5)

      for image in os.listdir(os.path.join(self.ablsolute_path, 'images')):
        self.images.append(os.path.join(self.ablsolute_path, 'images', image))

      if len(self.images) > 4:
        prompt = fr"""
        #Grounding Instruction.
        You are the eyes of a system that is trying to understand the world. you receive images every few seconds and just respond with imporatnt insights about the image. for the sysystem to properly understand what it needs, you also receive your previous outputs to help you better understand the concept of motion.

        #Previous Observations.
        {last_5_perceptions}

        # Note: The Observatiosn can be empty if the system is just starting up.

        Current Time: {datetime.now().strftime("%H:%M:%S")}
        """
        last_5_images = self.images[-3:]
        
        try:
          modelinsights = self.generate_insights(last_5_images, prompt)

          insights = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'insights': modelinsights
          }

          self.perceptions.append(fr'observation: {insights}, Date_of_observation: {datetime.now().strftime("%H:%M:%S")}')
          os.system('clear')
          
          print(insights)


          self.delete_images(last_5_images)
          time.sleep(1.5)
        except Exception as e:
          print('Experiencing an error,', e, ' \n Retrying in 1.5 seconds...')
          time.sleep(1.5)
          continue
      else:
        print('waiting')
        continue

if __name__ == '__main__':
  vision_engine = VisionEngine()
  vision_engine.insights_loop()