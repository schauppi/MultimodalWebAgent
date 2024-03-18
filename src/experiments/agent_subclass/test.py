from src.experiments.agent_subclass.multimodal_websurfer import MultimodalWebsurfer
from src.autogen_configuration.autogen_config import GetConfig

from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, Agent

llm_config = GetConfig().config_list

websurfer = MultimodalWebsurfer(
    name="MultimodalWebsurfer",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    llm_config=llm_config,
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    is_termination_msg=lambda x: True,
)


task1 = """
Search the web for information about Microsoft AutoGen
"""

user_proxy.initiate_chat(websurfer, message=task1)
