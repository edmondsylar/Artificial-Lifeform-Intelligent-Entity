from SystemApis.BridgeController import *



# create functino to get the conversations for a given layer
def wrapper_get_conversation(layer, limit):
    # Additional behavior before the original function call can be added here
    result = get_conversation(layer, limit)
    # Additional behavior after the original function call can be added here
    return result


def wrapper_insert_conversation(layer, role, content):
    # Additional behavior before the original function call can be added here
    result = insert_conversation(layer, role, content)
    # Additional behavior after the original function call can be added here
    return result