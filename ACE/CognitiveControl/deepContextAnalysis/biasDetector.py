# function transforms the prompt into the required format.

def sentimentDetection(context, text):

    _promtTemplate = f"""
    This is your Oprating configuration to help you better have self awareness and purpose.
    {context}
    NOTE: At this layer level you are strictly for Sentiment Detection.
    Base on the above configuration to answer the Below:
    
    Can you please detect the sentiment of the passed information:
    information:  {text}

    Note: The sentiment can be either positive or negative and explain why you think so.


    """ 

    return (_promtTemplate)

