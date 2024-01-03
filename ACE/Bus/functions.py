import requests
import json

def post_data_to_bus(table, data):
    url = 'http://localhost:5012/bus_p'
    payload = {
        'table': table,
        'data': data
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    return response.json()

def get_data_from_bus(table, limit):
    url = 'http://localhost:5012/bus_g'
    payload = {
        'table': table,
        'params': {
            'limit': limit
        }
    }
    headers = {'content-type': 'application/json'}
    response = requests.get(url, data=json.dumps(payload), headers=headers)
    return response.json()


def create_and_fetch_recent(table, data):
    # Create the record
    post_data_to_bus(table, data)

    # Fetch all records
    all_records = get_data_from_bus(table, 6)

    # If there are less than 6 records, return all of them
    if len(all_records) < 6:
        return all_records

    # Otherwise, return the most recent 6 records
    return all_records[-6:]