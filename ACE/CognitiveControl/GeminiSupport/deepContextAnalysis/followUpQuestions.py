# function transforms the prompt into the required format.

def compose_followUpGen_prompt(context, text):

    _promtTemplate = f"""
    This is your Oprating configuration to help you better have self awareness and purpose.
    {context}
    NOTE: At this layer level you are strictly To Develop possible follow up questions for the passed topic
    Base on the above configuration to answer the Below:

    Please generate related follow-up questions to this topic: 
    
    {text}
    """

    return (_promtTemplate)

