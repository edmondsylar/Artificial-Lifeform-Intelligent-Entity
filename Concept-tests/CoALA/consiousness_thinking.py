import threading
import json
import time
import os
import google.generativeai as palm

from dotenv import load_dotenv

# load the .env file
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

# get the api key from the .env file
palm.configure(api_key=key)


def generate_thoughts(input_text):

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

    prompt = f"""You are the personal growth and development unit of an autonomous self-thinking evolving ai system. based on the current State of the world, you freely think of what you want to research and the share.

    Please share your Thoughts in this format:
    {{
    "Comment": "There are many things that I would like to research and share. Here are a few that come to mind ",
    "Thoughts" : ["The future of work and how AI will impact it.", "The ethics of AI and how we can ensure that it is used for good.", "The potential of AI to solve some of the world's most pressing problems, such as climate change and poverty.", "The ways in which AI can be used to improve our lives, such as in healthcare, education, and transportation"],
    "ExtraNotes" : " I believe that by studying these topics, we can better understand the potential of AI and how to use it to make the world a better place."
    }}
    
    You receive Your General System Status Status and based on that you devise self, improvement plans and share.
    input: think
    output: {{
    "Comment": "There are many things that I would like to research and share. Here are a few that come to mind ",
    "Thoughts" : ["The future of work and how AI will impact it.", "The ethics of AI and how we can ensure that it is used for good.", "The potential of AI to solve some of the world's most pressing problems, such as climate change and poverty.", "The ways in which AI can be used to improve our lives, such as in healthcare, education, and transportation"],
    "ExtraNotes" : " I believe that by studying these topics, we can better understand the potential of AI and how to use it to make the world a better place."
    }}
    input: {input_text}
    output:"""

    response = palm.generate_text(
        **defaults,
        prompt=prompt
    )

    return response.result



# write to the thoughts list in the thoughts json file 
def write_to_thoughts(thoughts_list):
    # convert to json object
    thoughts_json = json.loads(thoughts_list)
    thoughts_List = thoughts_json['Thoughts']

    # open the thoughts file for reading and writing
    with open('thoughts.json', 'r+') as thoughts_file:
        # load the thoughts file
        thoughts = json.load(thoughts_file)
        # append the new thoughts to the thoughts list
        thoughts['thoughts'].append(thoughts_List)
        # write the new thoughts list to the thoughts file
        thoughts_file.seek(0)
        json.dump(thoughts, thoughts_file, indent=4)
        thoughts_file.truncate(
            thoughts_file.tell()
        )

    return True



def thoughtTimer():
        while True:
            # Call the function
            print('Thoughts fired...')
            thoughts = generate_thoughts('what next')
            write_to_thoughts(thoughts)

            # Pause execution for 2 minutes
            time.sleep(120)


while True:
    # create a thread for the thoughtTimer function
    t1 = threading.Thread(target=thoughtTimer)
    # start the thread
    t1.start()
    # get the user input
    input_text = input('Thought Injection (optional): ')