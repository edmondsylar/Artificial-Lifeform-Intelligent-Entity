import google.generativeai as palm
import os 
from dotenv import load_dotenv

key = os.getenv("GOOGLE_NLP_KEY")

palm.configure(api_key=key)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}



# creat a function that takes in the input and returns the output.

def _ami_required(input):
    prompt = fr"""
        You are a vision identifier model which only determines if the passed request requires the use of the camera and for what.
        Example:
        your response to questions strictly as follows:
        {{
        "required_camera: "true",
        "type": "picture",
        }}

        or 

        {{
        "required_camera: "true",
        "type": "video",
        }}

        or 

        {{
        "required_camera: "False",
        "type": "none",
        }}

        input: hello man
        output: {{
        "required_camera: "False",
        "type": "none",
        }}
        input: Please check this image out for me
        output: {{
        "required_camera: "true",
        "type": "picture",
        }}
        input: hey take a look at this 
        output: {{
        "required_camera: "true",
        "type": "video",
        }}
        input: {input}
        output:
    """
    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    print(response.result)

_ami_required("hey man i need to check the image out for me")