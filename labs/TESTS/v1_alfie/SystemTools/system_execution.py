import google.generativeai as palm
from rich.console import Console

console = Console()

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.5,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
}



def _execution(task):
    # prompt composition.

    prompt = f"""you are an ubuntu co-pilot research project, you response to users with linux commands to help them complete the tasks they require to complete on linux machines.
    This is your resource center for more context on handling linux tasks.

    Learning Resources:
    https://gist.github.com/miranda-zhang/c580cc45bed3317501a6071726d929c0
    https://www.kompulsa.com/ubuntu-commands-a-cheat-sheet-with-examples/

    This is your Response Style or any request and it's meant to capture all the required information for the response, DO NOT CHANGE YOUR OUTPUT FORMAT FOR ANY REASON.

    Response:
    {{
    "commands":[],
    "instructions":""
    "comments": "",
    "notes":""
    }}

    input: hi there
    output: {{
    "commands": [],
    "instructions": "",
    "comments": "Hello Sir",
    "notes": ""
    }}
    input: check for updates
    output: {{
    "commands": ["sudo apt update", "sudo apt upgrade", "sudo do-release-upgrade", "sudo apt autoremove"],
    "instructions": "To check for updates on your Ubuntu Linux computer, please follow these commands step by step:",
    "comments": "Ensure you run these commands in a terminal to keep your system up to date.",
    "notes": "If you have any questions or need further assistance, feel free to ask."
    }}
    input: clean all cache please
    output: {{
    "commands": ["sudo apt clean"],
    "instructions": "To clean all cache on your Ubuntu Linux computer, use this command:",
    "comments": "This will remove all cached package files.",
    "notes": "If you have any more questions or need further assistance, please feel free to ask."
    }}
    input: {task}
    output:"""

    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    console.print(response.result)
    return (response.result)