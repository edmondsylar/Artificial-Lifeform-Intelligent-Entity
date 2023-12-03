# function transforms the prompt into the required format.

def compose_goals_prompt(context, goal):

    _promtTemplate = f"""
    This is your Oprating configuration to help you better have self awareness and purpose.
    {context}
    NOTE: At this layer level you are strictly To Develop goals in respect to the passed prompt
    Base on the above configuration to answer the Below:

    Please generate the possible goals for the following prompt: 
    
    {goal}
    """

    return (_promtTemplate)



