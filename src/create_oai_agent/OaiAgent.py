import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import openai

from src.utils.logging.log_config import setup_logging
from src.create_oai_agent.ToolDefinitionFactory import ToolDefinitionFactory

setup_logging()
logger = logging.getLogger(__name__)


class OAIAssistantCreator:
    """
    Class responsible for creating an OpenAI assistant with specified tools and instructions.
    """

    def __init__(self, dotenv_path, config_path, instruction_path, assistant_save_path):
        """
        Initialize the creator with paths to necessary configurations and instructions.
        """
        self.dotenv_path = dotenv_path
        self.config_path = config_path
        self.instruction_path = instruction_path
        self.assistant_save_path = assistant_save_path
        self.client = None
        logger.info(
            "OAIAssistantCreator initialized with config and instruction paths.")

    def load_environment(self) -> None:
        """
        Load environment variables from the .env file.

        Args:
            None

        Returns:
            None
        """
        try:
            load_dotenv(dotenv_path=self.dotenv_path)
            logger.info("Environment variables loaded successfully.")
        except Exception as e:
            logger.error("Failed to load the .env file.", exc_info=True)

    def initialize_openai_client(self) -> None:
        """
        Initialize the OpenAI client with the API key from environment variables.

        Args:
            None

        Returns:
            None
        """
        try:
            self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            logger.info("OpenAI client initialized successfully.")
        except KeyError as e:
            logger.error(
                "OPENAI_API_KEY not found in environment variables.", exc_info=True)
            raise

    def load_instructions(self) -> str:
        """
        Load instructions for the assistant from the specified JSON file.

        Args:
            None

        Returns:
            str: The loaded instructions.
        """
        try:
            with open(self.instruction_path, 'r') as file:
                instruction = json.load(file)["instruction"]
            logger.info("Instructions loaded successfully.")
            return instruction
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error("Failed to load instructions.", exc_info=True)
            raise

    def create_assistant(self) -> str:
        """
        Create an OpenAI assistant with the loaded tools and instructions.

        Args:
            None

        Returns:
            str: The ID of the created assistant.
        """
        try:
            factory = ToolDefinitionFactory(self.config_path)
            oai_tools = [factory.create_tool_definition(
                tool_type) for tool_type in factory.config]

            instruction = self.load_instructions()
            assistant = self.client.beta.assistants.create(
                model=os.environ.get('OPENAI_MODEL', ''),
                instructions=instruction,
                tools=oai_tools,
                name="BrowsingAgent"
            )
            logger.info(
                f"Assistant created successfully with ID: {assistant.id}")
            return assistant.id
        except Exception as e:
            logger.error("Failed to create assistant.", exc_info=True)
            raise

    def save_assistant_id(self, assistant_id: str) -> None:
        """
        Save the assistant's ID to a JSON file.

        Args:
            assistant_id (str): The ID of the assistant to save.

        Returns:
            None
        """
        data_to_append = {
            "type": "oai_browsing_assistant",
            "id": assistant_id,
            "date": str(datetime.now())
        }

        try:
            with open(self.assistant_save_path, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
            logger.info("Existing assistant data loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            data = []
            logger.info(
                "No existing assistant data found or error in loading; starting fresh.")

        data.append(data_to_append)

        with open(self.assistant_save_path, "w") as file:
            json.dump(data, file, indent=4)
            logger.info(f"Assistant ID {assistant_id} saved successfully.")

    def run(self) -> None:
        """
        Run the process of creating an assistant and saving its ID.

        Args:
            None

        Returns:
            None
        """
        logger.info("Starting the OAIAssistantCreator process.")
        self.load_environment()
        self.initialize_openai_client()
        assistant_id = self.create_assistant()
        self.save_assistant_id(assistant_id)
        logger.info("OAIAssistantCreator process completed successfully.")


if __name__ == "__main__":
    dotenv_path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), '..', '..', '.env'))
    config_path = 'src/create_oai_agent/utils/tool_definitions.json'
    instruction_path = 'src/create_oai_agent/utils/oai_instructions.json'
    assistant_save_path = "src/create_oai_agent/utils/assistant_id.json"

    creator = OAIAssistantCreator(
        dotenv_path, config_path, instruction_path, assistant_save_path)
    creator.run()
