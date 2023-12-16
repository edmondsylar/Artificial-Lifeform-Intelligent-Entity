import google.generativeai as genai
import os
from dotenv import load_dotenv
from .goals import compose_goals_prompt
from .followUpQuestions import compose_followUpGen_prompt
from .biasDetector import sentimentDetection
import threading
from rich.console import Console    

console = Console()

load_dotenv()

# get the API key from the .env file
API_KEY = os.getenv("google_gemini_api_key")


genai.configure(api_key=API_KEY)

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
}


deepContext = []

def contextDevelopment(property, prompt):
        response = genai.generate_text(
                **defaults,
                prompt=prompt
        )
        resp =  response.result

        # add the response to the deepContext list
        deepContext.append({
                "Property" : property,
                "Response" : resp
        })

        return resp


def deepContentEngineAnalysis(context, query):
    # follow up questions querry
    folloqUpQuery = compose_followUpGen_prompt(context, query)

    # goals querry
    goals = compose_goals_prompt(context, query)

    # bias check querry
    biasCheck = sentimentDetection(context, query)


    # create a thread for each of the queries
    thread1 = threading.Thread(target=contextDevelopment, args=("Goals", goals))
    thread2 = threading.Thread(target=contextDevelopment, args=("Follow Up Questions", folloqUpQuery))
    thread3 = threading.Thread(target=contextDevelopment, args=("Bias Check", biasCheck))

    # start the thread
    thread1.start()
    thread2.start()
    thread3.start()

    # wait for the thread to finish
    thread1.join()
    thread2.join()
    thread3.join()



    # print the deepContext list
#     console.print(deepContext)
    return deepContext


