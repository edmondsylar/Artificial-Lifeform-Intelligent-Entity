import os
import time
import google.generativeai as palm

import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

# authenitcate.
palm.configure(api_key=google_api_key)


defaults = {
  'model': 'tunedModels/alfiefrontallobe-kyq41pe4v89i',
  'temperature': 0.7,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}
input = 'Hi there'
prompt = f"""input: {input}
output:"""

response = palm.generate_text(
  **defaults,
  prompt=prompt
)
print(response.result)