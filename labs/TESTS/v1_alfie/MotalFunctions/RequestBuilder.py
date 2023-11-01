# we are going to have a function that builds the user request with all the relevant information.

def refine_request(user_request, frontalLobe_response):
    # we need to format the request together with the tasks being taken by the frontal Lobe.
    refined_request = f"""
    User has requested as follows:
    {user_request}. 

    The Frontal Lobe has received this request and is taking the following action to resolve.
    Frontal Lobe Response to request:
    {frontalLobe_response}
    """

    return refined_request