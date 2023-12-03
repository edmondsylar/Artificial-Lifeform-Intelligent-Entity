# this file is basically going to controlhow we innteract with the the main layer to pass the information from external sources to the main layer
import requests
import json
from dotenv import load_dotenv
import os
from rich.console import Console

load_dotenv()

console = Console()


# define the api url
db_api_url = os.getenv('db_api_url')

# define aspirational layer url
aspirational_layer_url = os.getenv('aspirational_layer_url')

def _interact():
    # get southound bus messages
    # define the url
    msgs = []

    url = db_api_url + '/south_bound_bus_get'
    try:
        # make the request
        response = requests.get(url)
        # check if the response is successful
        if response.status_code == 200:
            # return the response
            if response.json() != []:
                # convert for better processing
                for msg in response.json():
                    msgs.append({
                        "layer": msg[1],
                        "messages": msg[2]
                    })
                # completed getting the messages
            print(msgs)
            # input('Press enter to continue')
            # now we are going to call the aspirational layer and pass the messages to it
            # define the url
            url = aspirational_layer_url + '/aspirational_layer'
            # compose the data
            data = {
                "data": fr'{msgs}'
            }

            # make the request
            response = requests.post(url, json=data)
            print(response)
            return response

        else:
            # return the error
            return response.json()
        
    except Exception as e:
        # return the error
        return str(e)
    pass