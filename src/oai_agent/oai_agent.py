from src.configs.logging.logging_config import setup_logging
from src.oai_agent.utils.load_assistant_id import load_assistant_id
from src.oai_agent.utils.create_oai_agent import create_agent
from src.autogen_configuration.autogen_config import GetConfig
from src.tools.read_url import read_url
from src.tools.scroll import scroll
from src.tools.jump_to_search_engine import jump_to_search_engine
from src.tools.go_back import go_back
from src.tools.wait import wait
from src.tools.click_element import click_element
from src.tools.input_text import input_text
from src.tools.analyze_content import analyze_content
from src.tools.save_to_file import save_to_file
from src.oai_agent.utils.prompt import prompt

import logging
import autogen
from autogen.agentchat import AssistantAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

import openai

setup_logging()
logger = logging.getLogger(__name__)


def configure_agent(assistant_type: str) -> GPTAssistantAgent:
    """
    Configure the GPT Assistant Agent with the specified tools and instructions.

    Args:
        None

    Returns:
        GPTAssistantAgent: An instance of the GPTAssistantAgent.
    """
    try:
        logger.info("Configuring GPT Assistant Agent...")
        assistant_id = load_assistant_id(assistant_type)
        llm_config = GetConfig().config_list
        oai_config = {
            "config_list": llm_config["config_list"], "assistant_id": assistant_id}
        gpt_assistant = GPTAssistantAgent(
            name=assistant_type, instructions=AssistantAgent.DEFAULT_SYSTEM_MESSAGE, llm_config=oai_config
        )
        logger.info("GPT Assistant Agent configured.")
        return gpt_assistant
    except openai.NotFoundError:
        logger.warning("Assistant not found. Creating new assistant...")
        create_agent(assistant_type)
        return configure_agent()
    except Exception as e:
        logger.error(f"Unexpected error during agent configuration: {str(e)}")
        raise


def register_functions(agent):
    """
    Register the functions used by the GPT Assistant Agent.

    Args:
        agent (GPTAssistantAgent): An instance of the GPTAssistantAgent.

    Returns:
        None
    """
    logger.info("Registering functions...")
    function_map = {
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
    agent.register_function(function_map=function_map)
    logger.info("Functions registered.")


def create_user_proxy():
    """
    Create a User Proxy Agent.

    Args:
        None

    Returns:
        UserProxyAgent: An instance of the UserProxyAgent.
    """
    logger.info("Creating User Proxy Agent...")
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
    )
    logger.info("User Proxy Agent created.")
    return user_proxy


def main():
    """
    Main function to run the GPT Assistant Agent.

    Args:
        None

    Returns:
        None
    """
    try:
        gpt_assistant = configure_agent("BrowsingAgent")
        register_functions(gpt_assistant)
        user_proxy = create_user_proxy()
        user_proxy.initiate_chat(
            gpt_assistant, message=prompt)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
