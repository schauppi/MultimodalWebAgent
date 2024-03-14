from src.oai_agent.utils.load_assistant_id import load_assistant_id
from src.autogen_configuration.autogen_config import GetConfig
from src.oai_agent.oai_agent import configure_agent

from src.tools.read_url import read_url
from src.tools.scroll import scroll
from src.tools.jump_to_search_engine import jump_to_search_engine
from src.tools.go_back import go_back
from src.tools.wait import wait
from src.tools.click_element import click_element
from src.tools.input_text import input_text
from src.tools.analyze_content import analyze_content
from src.tools.save_to_file import save_to_file

import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

browsing_agent_id = load_assistant_id("BrowsingAgent")
qa_agent_id = load_assistant_id("QualityAssuranceAgent")

llm_config = GetConfig().config_list

browsing_agent_config = {
    "config_list": llm_config["config_list"], "assistant_id": browsing_agent_id}

qa_agent_config = {
    "config_list": llm_config["config_list"], "assistant_id": qa_agent_id}

browsing_agent = GPTAssistantAgent(
    name="browsing_agent", llm_config=browsing_agent_config)

qa_agent = GPTAssistantAgent(
    name="qa_agent", llm_config=qa_agent_config)

print(browsing_agent.get_assistant_instructions())

print("-----")

print(qa_agent.get_assistant_instructions())

browsing_agent_function_map = {
    "analyze_content": analyze_content,
    "click_element": click_element,
    "go_back": go_back,
    "input_text": input_text,
    "jump_to_search_engine": jump_to_search_engine,
    "read_url": read_url,
    "scroll": scroll,
    "wait": wait,
    "save_to_file": save_to_file,
}

qa_agent_function_map = {
    "analyze_content": analyze_content,
}

browsing_agent.register_function(browsing_agent_function_map)
qa_agent.register_function(qa_agent_function_map)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
    llm_config=llm_config,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

groupchat = autogen.GroupChat(agents=[user_proxy, browsing_agent, qa_agent], messages=[
], max_round=30, speaker_selection_method="round_robin")

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

prompt = """

TASK: Go to the Amazon website and search for a laptop, filter for laptops with more than 4 stars, select the first and put in in the cart.


"""


user_proxy.initiate_chat(
    manager,
    message=prompt,
)
