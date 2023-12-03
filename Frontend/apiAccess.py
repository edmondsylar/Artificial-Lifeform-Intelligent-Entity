# we are going to have function that will be used to access the api and return the data
import requests
import json
import os
import threading
from dotenv import load_dotenv

load_dotenv()

# define the api url
db_api_url = os.getenv('db_api_url')

def post_to_southbound_bus(data):
    # we are going to call the endpoint for posting to the southbound bus
    # /south_bound_bus_insert

    # define the url
    url = db_api_url + '/south_bound_bus_insert'
    try:
        # make the request
        response = requests.post(url, json=data)
        # check if the response is successful
        if response.status_code == 200:
            # return the response
            print(response)
            return response
        else:
            # return the error
            return response
        
    except Exception as e:
        # return the error
        return str(e)

    pass