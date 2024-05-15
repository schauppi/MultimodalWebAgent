from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel
import logging
import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
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

import openai
from autogen.agentchat import AssistantAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from fastapi.middleware.cors import CORSMiddleware

import websockets
import json
import requests

from src.webdriver.webdriver import WebDriver

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PromptRequest(BaseModel):
    prompt: str

setup_logging()
logger = logging.getLogger(__name__)

def configure_agent(assistant_type: str) -> GPTAssistantAgent:
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


@app.post("/launch-browser")
def launch_browser():
    try:
        driver = WebDriver.getInstance()
        page = driver.getDriver()
        # Fetch all pages from the Chrome instance
        response = requests.get("http://localhost:9222/json")
        pages = response.json()

        # Assuming the last page in the list is the right-most tab
        if pages:
            right_most_page = pages[-1]  # Get the last tab/page
            if "webSocketDebuggerUrl" in right_most_page and right_most_page['type'] == 'page':
                websocket_url = right_most_page["webSocketDebuggerUrl"]
                return {"websocket_url": websocket_url, "right_most_page": right_most_page}
            else:
                raise Exception("Right-most page does not have a WebSocket URL")
        else:
            raise Exception("No pages found in the browser session")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/get-web-agent-response")
def get_response(prompt_request: PromptRequest):
    try:
        gpt_assistant = configure_agent("BrowsingAgent")
        register_functions(gpt_assistant)
        user_proxy = create_user_proxy();

        # driver = WebDriver.getInstance()
        # page = driver.getDriver()
        # page.goto("https://www.amazon.com/")

        # page.waitFor(10000)

        # response = {"data": "Hello, how can I help you?"}
        response = user_proxy.initiate_chat(gpt_assistant, message=prompt_request.prompt)
        return {"response": response}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.websocket("/cdp")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # The URL should now be directly passed or managed correctly in the session
        ws_url = await websocket.receive_text();

        async with websockets.connect(ws_url) as browser_ws:
            async def to_browser():
                try:
                    async for message in websocket.iter_text():
                        await browser_ws.send(message)
                except Exception as e:
                    logger.error(f"Error in to_browser: {str(e)}")

            async def from_browser():
                try:
                    async for message in browser_ws:
                        await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error in from_browser: {str(e)}")

            await asyncio.gather(to_browser(), from_browser())
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
