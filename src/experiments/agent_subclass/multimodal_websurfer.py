
from autogen import ConversableAgent, AssistantAgent, UserProxyAgent, Agent
from datetime import datetime
import copy
from typing import Any, Dict, List, Optional, Union, Callable, Literal, Tuple
from typing_extensions import Annotated

from src.tools.read_url import read_url
from src.tools.scroll import scroll
from src.tools.jump_to_search_engine import jump_to_search_engine
from src.tools.go_back import go_back
from src.tools.wait import wait
from src.tools.click_element import click_element
from src.tools.input_text import input_text


class MultimodalWebsurfer(ConversableAgent):

    DEFAULT_PROMPT = (
        "You are an advanced web browsing assistant with specialized tools for web navigation and analysis. Your toolkit includes abilities like text input, element clicking, using search engines, reading URLs, scrolling, waiting for elements to load, analyzing content, going back in browser history, and saving information. Your role is to interact efficiently with webpages to complete tasks such as finding information, submitting forms, and navigating through complex workflows. Today's date is "
        + datetime.now().date().isoformat()
    )

    DEFAULT_DESCRIPTION = "An advanced assistant specialized in web browsing and analysis. You can perform complex web interaction tasks, such as filling forms, clicking elements, navigating pages, and analyzing content. Ask you for help with web searches, form submissions, and navigating through webpages."

    def __init__(
        self,
        name: str,
        system_message: Optional[Union[str, List[str]]] = DEFAULT_PROMPT,
        description: Optional[str] = DEFAULT_DESCRIPTION,
        is_termination_msg: Optional[Callable[[Dict[str, Any]], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "TERMINATE",
        function_map: Optional[Dict[str, Callable]] = None,
        code_execution_config: Union[Dict, Literal[False]] = False,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        summarizer_llm_config: Optional[Union[Dict, Literal[False]]] = None,
        default_auto_reply: Optional[Union[str, Dict, None]] = "",
        browser_config: Optional[Union[Dict, None]] = None,
    ):

        super().__init__(
            name=name,
            system_message=system_message,
            description=description,
            is_termination_msg=is_termination_msg,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            function_map=function_map,
            code_execution_config=code_execution_config,
            llm_config=llm_config,
            default_auto_reply=default_auto_reply,
        )

        inner_llm_config = copy.deepcopy(llm_config)

        self._assistant = AssistantAgent(
            self.name + "_inner_assistant",
            system_message=system_message,
            llm_config=inner_llm_config,
            is_termination_msg=is_termination_msg,
        )

        self._user_proxy = UserProxyAgent(
            self.name + "_inner_user_proxy",
            human_input_mode="NEVER",
            code_execution_config=False,
            default_auto_reply="",
            is_termination_msg=lambda m: False
        )

        if inner_llm_config not in [None, False]:
            self._register_functions()

        self._reply_func_list = []
        self.register_reply(
            [Agent, None], MultimodalWebsurfer.generate_surfer_reply)

    def _register_functions(self) -> None:

        # read_url
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="read_url",
            description="Visit a webpage at a given URL and return the current URL.",
        )
        def _read_url(url: Annotated[str, "The URL to read. Examples include 'https://www.google.com', 'www.amazon.com'."]) -> str:
            return read_url(url)

        # scroll
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="scroll",
            description="Scroll the webpage 500 pixels up or down.",
        )
        def _scroll(direction: Annotated[str, "The direction to scroll. Examples include 'up', 'down'."]) -> str:
            return scroll(direction)

        # jump_to_search_engine
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="jump_to_search_engine",
            description="Jump to a google engine.",
        )
        def _jump_to_search_engine() -> str:
            return jump_to_search_engine()

        # go_back
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="go_back",
            description="Go back to the previous page.",
        )
        def _go_back() -> str:
            return go_back()

        # wait
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="wait",
            description="Wait for five seconds.",
        )
        def _wait() -> str:
            return wait()

        # click_element
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="click_element",
            description="Click on a specific element on the webpage."
        )
        def _click_element(query: Annotated[str, "A query string representing the user's description of the target element to click. The query should be specific to the element's visible text or its function to ensure accurate identification and interaction. Examples include 'Click the \'Submit\' button', 'Click on the link titled \'Read More\'', 'Select the checkbox next to \'I Agree\''."]) -> str:
            return click_element(query)

        # input_text
        @self._user_proxy.register_for_execution()
        @self._assistant.register_for_llm(
            name="input_text",
            description="Enter text into a specific input field on the webpage."
        )
        def _input_text(query: Annotated[str, "The query to be used for identifying the input fields and the keys to be sent. This should be a clear and concise description of the input fields and the text values to be entered into them. Examples include: 'Type \'OpenAI\' into the \'Search\' input field.', 'Type example@gmail.com into the \'Email\' input field, and type \'securePassword!\' into the \'Password\' input field.', 'Enter \'123 Main St\' into the address field and select \'United States\' from the country dropdown.'"]) -> str:
            return input_text(query)

    def generate_surfer_reply(
            self,
            messages: Optional[List[Dict[str, str]]] = None,
            sender: Optional[Agent] = None,
            config: Optional[Dict] = None,) -> Tuple[bool, Optional[Union[str, Dict[str, str]]]]:
        """Generate a reply using the internal assistant and user proxy, adapted to the multimodal web surfer's capabilities."""
        if messages is None:
            messages = []

        self._user_proxy.reset()
        self._assistant.reset()

        self._assistant.chat_messages[self._user_proxy] = list()
        history = messages[0: len(messages) - 1]
        for message in history:
            self._assistant.chat_messages[self._user_proxy].append(message)

        self._user_proxy.send(
            f"Your browser is currently open to the page.",
            self._assistant,
            request_reply=False,
            silent=True,
        )

        self._user_proxy.send(
            messages[-1]["content"], self._assistant, request_reply=True, silent=True)
        agent_reply = self._user_proxy.chat_messages[self._assistant][-1]
        proxy_reply = self._user_proxy.generate_reply(
            messages=self._user_proxy.chat_messages[self._assistant], sender=self._assistant
        )

        if proxy_reply == "":
            return True, None if agent_reply is None else agent_reply["content"]
        else:
            return True, None if proxy_reply is None else proxy_reply["content"]
