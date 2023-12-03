# this is the main file for the internet search agent
import requests
import json
from rich.console import Console

console = Console()

url = "https://google.serper.dev/search"


def search(query):
    payload = json.dumps({
    "q": f"{query}"
    })
    headers = {
    'X-API-KEY': '4ae7638e2b578f791a3c51757fbd77094d145d57',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # convert the response to a json object 
    try:
        resp = json.loads(response.text)
        results = resp
        console.print(type(results["searchParameters"]), results["knowledgeGraph"])
        return results["knowledgeGraph"]

    except Exception as er:
        console.print(f"Error: Could not parse response, {er}")
        return


search("when was donald trump born")