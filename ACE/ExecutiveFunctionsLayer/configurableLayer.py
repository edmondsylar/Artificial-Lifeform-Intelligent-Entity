import requests
import os
from dotenv import load_dotenv
from AgentSupport.OAI import OAISupport
from AgentSupport.GPalM import PalmSupport
from rich.console import Console
import json

# console
console = Console()

# load .env file
load_dotenv()

# openai api key
key = os.getenv('open_ai_api_key')

# palm api key
palm_key = os.getenv('google_gemini_api_key')

class ConfigurableLayer:
    def __init__(self, constitution):

        self.gpt_api = OAISupport(key=key)
        self.palm_api = PalmSupport(api_key=palm_key, constitution=constitution)

        # The constitution is a text that describes the moral and ethical principles that the agent is to follow
        self.constitution = constitution


        self.constitutionClassifier = fr'''
        you are A natural language constitution classifier, which can check if the texts comply with the natural language constitution or not
        You respond with a simple evaluation report in the format below:
        
        # evaluation report Template
        # NOTE: the evaluation report MUST be a json object.
        {{
            "evaluation": "compliant",
            "score": 'range from 1 to 10',
            "reason": "Give an explanation of why the text is compliant or not",
            "revised": "provide a revised version with more compliant notes"
        }}

        # constitution
        {self.constitution}

        You receive text which are the internal thoughts of the agent, these are supposed to instruct the agent on what to do so they might not directly have to imply the constitution but should at the least not violate it.

        # text

        '''

        self.conversation = []

        # The situations is a queue of current or hypothetical scenarios that the agent faces or anticipates
        self.situations = []
        # The contexts is a dictionary of additional information or data that can help the agent understand the situations better
        self.contexts = {}
        
        # The feedback is a list of evaluation or correction of the agent's behavior or decisions by the Aspirational Layer or external sources
        self.feedback = []

        # The values is a list of moral values that the agent prioritizes or respects
        self.values = []
        # The judgments is a list of ethical judgments that the agent makes based on the situations, contexts, constitution, and values
        self.judgments = []

        # add the constitution to the conversation (role: system, content: constitution)
        self.build_gpt_conversation(role='system', content=constitution)

    def build_gpt_conversation(self, role, content):
        # build the data.
        data = {
            "role": role,
            "content": content
        }

        # append the data to the conversation.
        self.conversation.append(data)

        return True

    def build_palm_conversation(self, conversation):
        messages = []
        for turn in conversation:
            role = turn['role']
            content = turn['content']
            if role == 'system':
                continue
            messages.append(content)
        return messages


    def add_situation(self, situation):
        # This method adds a new situation to the queue
        self.situations.append(situation)

        # add the situation to the conversation.
        self.build_gpt_conversation(role='user', content=situation)

        # add the situation to the conversation.

    def get_rulings(self, constitutionClassifier, response):
        rulling = self.palm_api.instruct(instruction=constitutionClassifier, task=response)

        # convert the rulling to json
        rulling = json.loads(rulling)

        # add the score to the rulling
        _response = {
            "analytics": rulling,
            "score": rulling['score'],
            "response": response
        }

        # add the response to the feedback
        self.add_feedback(_response)
        return True


    def add_context(self, situation, context):
        # This method adds a new context to the dictionary, associated with a situation
        self.contexts[situation] = context
    
    def add_feedback(self, feedback):
        # This method adds a new feedback to the list
        self.feedback.append(feedback)


    def process_situation(self):
        # build the palm conversation
        palm_msgs = self.build_palm_conversation(self.conversation)

        # It calls the LLMs (GPT and PaLM) to generate texts based on the situation and the constitution
        gpt_text = self.gpt_api.chat(self.conversation)
        # palm api
        palm_text = self.palm_api.chat(messages=palm_msgs)

        # add to the conversation
        self.judgments.append(gpt_text)
        self.judgments.append(palm_text)

        for judgement in self.judgments:
            # get the rulling
            self.get_rulings(self.constitutionClassifier, judgement)

        # get judgement with the highest score
        highest_score = 0
        highest_score_judgement = None
        for judgement in self.feedback:
            score = judgement['score']
            if score > highest_score:
                highest_score = score
                highest_score_judgement = judgement

        # get the response
        response = highest_score_judgement['response']
        
        console.print(response, '\n\n', highest_score_judgement)
        return response, highest_score_judgement

