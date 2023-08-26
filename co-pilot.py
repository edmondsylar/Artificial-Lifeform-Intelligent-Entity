import openai 
from rich.console import Console
import os
from dotenv import load_dotenv


# set api key.
load_dotenv() 
openai.api_key = os.getenv('OPENAI_API_KEY')

printer = Console()
def log(text):
    return printer.log(text)

model_instructions = """
you are an Ubuntu terminal ai- copilot whose main role is to let assist users get things done in quickly.
your response style to users is formatted like this;


{
"commands" : [commands],
"single Execution Command: [commbined_command] // all commands are combined to make one executable command
"instructions" : " Execution instruction"
}
"""

#{"role": "user", "content": "Who won the world series in 2020?"},
#{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#{"role": "user", "content": "Where was it played?"}


class CoPilot_v_0:
    def __init__(self, LoggedInUser):
        self.user = LoggedInUser
        self.instruction = model_instructions
        self.history = []
        
        # add the instruction to the history
        self.history.append(
            {"role": "system", "content": self.instruction}
            )

    def build_context(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def exceutor(self, command):
        # exceute passed command.
        os.system(command)
        resp = "Execution completed"
        printer.log(resp)
        return resp

    def ai_query(self, user_prompt):

        # build user content
        self.build_context("user", user_prompt)

        ai_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.history
        )

        return ai_response 



co_pilot = CoPilot_v_0("user")
# printer.log(current_user)
while True:
    user_prompt = input(f"Alfie :> ")
    response = co_pilot.ai_query(user_prompt)
    ai_response  = response['choices'][0]['message']['content']

    # build context
    co_pilot.build_context("assistant", ai_response)
    log(ai_response)

    log("Would you like to execute the command?")
    resp = input(" [Y/N] >: ")


