from time import sleep
import os
import google.generativeai as palm
palm.configure(api_key="AIzaSyDn2fvOXSrPnm7hxCYQKwClE93hWfk8ch0")
from rich.console import Console
from functions.main_functions import build_prompt

console = Console()


co_pilot_defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0,
  'candidate_count': 2,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}
passed_data = 'Check all running services, dump the status in a file and name it services'

def _copilot(pt):
    prompt = build_prompt(pt)

    response = palm.generate_text(
    **co_pilot_defaults,
    prompt=prompt
    )
    return response
