from MotalFunctions.FrontalLobe import frontal_lobe
from rich.console import Console
from InfoProcessors.WorkDistributorModule import _receiver
import json

console = Console()

# This is our Entry point to the application.
print("ALFIE (preview-0.0.1)")
while True:
    user_request = input("_:> ")

    # call the frontal_lob
    response = frontal_lobe(user_request)
    console.print(response, type(response))

    if isinstance(response, dict):
        tools = response['tools']
        # pass this to the receiver.
        _receiver(tools=tools, instruction=response['instruction'])

    
    