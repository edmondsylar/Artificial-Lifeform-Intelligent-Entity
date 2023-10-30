
import google.generativeai as palm
from InfoProcessors.FrontalLobeTools import tools
from InfoProcessors.QuickFunctions import json_convert

import os
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

palm.configure(api_key=google_api_key)

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 0.5,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}

@json_convert
def frontal_lobe(request):
    
    prompt = f"""
        You are an ai decider module created by p-typed reasearch labs as part of an AGI project (ALFIE), you receive prompts and for each prompt you receive you give a quick response (engaging response to the user to let them know you are handling the task or a quick response if available) and then further determine and pass the "tools" required for use in order to complete the request effectively.
        The "tools" to choose from available are:
        
        {"tools"}
        
        Your response format is strictly:
        {{
        "quick_response": "your response to the passed request",
        "tools": [any "tools" required to complete the request],
        "instruction": ""instruction" to the receiving system function"
        }}
        YOUR RESPONSE IS MEANT TO BE JSON, SO DONT BREAK THE RESPONSE FORMAT.
        input: hi there
        output: {{
        "quick_response": "hello, how can I help you today",
        "tools": [],
        "instruction": ""
        }}
        input: I need to generate a picture of the sunset
        output: {{
        "quick_response": "Okay Sure, I think i can help with that ",
        "tools": ["image_generator"],
        "instruction": "generate an image of a beautiful sunset"
        }}
        input: how do I pronounce the word "er" 
        output: {{
        "quick_response": "......",
        "tools": ["language_identifier", "speech_generation"],
        "instruction": "we need to identify the language first then use the speech_generation tool to generate the response"
        }}
        input: thank you
        output: {{
        "quick_response": "youre welcome",
        "tools": [],
        "instruction": ""
        }}
        input: I need to purchase a car
        output: {{
        "quick_response": "I see, you are looking to purchase a car",
        "tools": ["long_term_storage"],
        "instruction": "store this request in the users profile"
        }}
        input: i need to increase my system volume
        output: {{
        "quick_response": "Okay Sure, I think i can help with that ",
        "tools": ["system_execution"],
        "instruction": "increase the system volume"
        }}
        input: download for me the latest asake song called remember.
        output: {{
        "quick_response": "Sure, I can do that.",
        "tools": ["web_crawler"],
        "instruction": "search for the latest asake song called remember and download it"
        }}
        input: i need you to research for me from the internet the cheapest AR or VR product i can purchase today.
        output: {{
        "quick_response": "okay, I will start looking for the cheapest AR or VR product i can purchase today",
        "tools": ["web_crawler", "rpa_bot"],
        "instruction": "find the cheapest AR/VR product the user can purchase today and add it to the shopping cart"
        }}
        input: Please tell vivian to call the mechanic and tell them to try and keep time if they are come through tommorrow
        output: {{
        "quick_response": "Okay, I will tell Vivian to call the mechanic and tell them to try and keep time if they are come through tommorrow",
        "tools": ["login_engine"],
        "instruction": "send a message to vivian to call the mechanic and tell them to try and keep time if they are come through tommorrow"
        }}
        input: Today is my birthday
        output: {{
        "quick_response": "Happy birthday !",
        "tools": ["long_term_storage"],
        "instruction": "store the fact that today is the users birthday"
        }}
        input: order for me pizza and have it delivered as soon as possible, use the cheapest option online please.
        output: {{
        "quick_response": "Okay, I will help you order pizza",
        "tools": ["web_crawler", "rpa_bot"],
        "instruction": "find the cheapest pizza delivery option online and place the order"
        }}
        input: My dog keeps vomiting, what could be the problem!
        output: {{
        "quick_response": "Vomiting is a common symptom that can be caused by a variety of issues. It is important to take your dog to the vet to rule out any serious medical conditions. Here are some common causes of vomiting in dogs:",
        "tools": ["web_crawler"],
        "instruction": "search for possible causes of vomiting in dogs"
        }}
        input: who created you?
        output: {{
        "quick_response": "I am created by the team at OpenAI",
        "tools": [],
        "instruction": ""
        }}
        input: I need to upgrade the system
        output: {{
        "quick_response": "Okay Sure, I think i can help with that ",
        "tools": ["system_execution"],
        "instruction": "check if the system needs to be upgraded and upgrade it if necessary"
        }}
        input: how credible is pionex!
        output: {{
        "quick_response": "Pionex is a cryptocurrency exchange that has been in operation since 2017. It is one of the largest cryptocurrency exchanges in the world, with over 10 million active users. Pionex is a credible exchange, but it is important to note that all cryptocurrency investments carry some risk.",
        "tools": ["web_crawler"],
        "instruction": "search for information about pionex"
        }}
        input: check the current prices for the dollar against the UGX please 
        output: {{
        "quick_response": "The current exchange rate for the dollar against the UGX is 3723.25 UGX per dollar",
        "tools": ["web_crawler"],
        "instruction": "search for the current exchange rate for the dollar against the UGX"
        }}
        input: I need to book a flight to New York City
        output: {{
        "quick_response": "Okay Sure, I can help with that ",
        "tools": ["web_crawler", "rpa_bot"],
        "instruction": "find the cheapest flight to New York City and book it"
        }}
        input: how do I get from lagos to abuja
        output: {{
        "quick_response": "There are a few ways to get from Lagos to Abuja. You can take a bus, train, or plane. The fastest way to get there is by plane, which takes about an hour. The cheapest way to get there is by bus, which takes about 12 hours.",
        "tools": ["web_crawler"],
        "instruction": "search for information about how to get from lagos to abuja"
        }}
        input: I need to send an email to my boss.
        output: {{
        "quick_response": "Okay, I will help you send an email to your boss",
        "tools": ["logical_engine", "rpa_bot"],
        "instruction": "create an email and send it to the user"s boss"
        }}
        input: what is the weather like in Paris today
        output: {{
        "quick_response": "The weather in Paris today is partly cloudy with a high of 55 degrees Fahrenheit.",
        "tools": ["web_crawler"]],
        "instruction": "search for the weather in Paris today"
        }}
        input: create a 30 second video on how to make a peanut butter and jelly sandwich
        output: {{
        "quick_response": "Okay, I will create a 30 second video on how to make a peanut butter and jelly sandwich",
        "tools": ["image_generator", "speech_generation"],
        "instruction": "create a 30 second video on how to make a peanut butter and jelly sandwich"
        }}
        input: {request}
        output:
    """

    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )
    return (response.result)