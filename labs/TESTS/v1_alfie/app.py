import google.generativeai as palm
import os
from dotenv import load_dotenv

# load the environment variables.
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# model to use
activeModel = 'models/text-bison-001',

# configure palm authentication
palm.configure(api_key=google_api_key)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.99,
  'candidate_count': 1,
  'candidate_count': 2,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 4000,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}


completion = palm.generate_text(
    **defaults,
    
)

outputs = [output['output'] for output in completion.candidates]

for output in outputs:
    print(output)
    print('-'*50)