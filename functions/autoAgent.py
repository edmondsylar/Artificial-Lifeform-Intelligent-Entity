import autogen 

config_list = [{'model': 'gpt-3.5-turbo-1106', 'api_key': ''},]

assistant = autogen.AssistantAgent(
    llm_config={
        "seed":42,
        "config_list":config_list,
        "temperature": 0.3,
    },
    name="thinker_module",
    )


# user_proxy
user_proxy = autogen.UserProxyAgent(
        name="tasker_module",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=15,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        # code_exectution_config={
        #     "work_dir": "agentWorkspace",
        #     "use_docker":False,
        # }
    )


user_proxy.initiate_chat(
    assistant,
    message="whats is the datw today? compare the year-to-date gain for META and TESLA, plot the chart and open  the completely png image."
)