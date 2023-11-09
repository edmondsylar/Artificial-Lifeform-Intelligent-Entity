import requests

# weather api.
def weather(location): 
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":f"{location}"}

    headers = {
        "X-RapidAPI-Key": "18531cc5femshe002bc3470f9b5ap1e6e98jsn2e42b35c1e99",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())