from src.create_oai_agent.oai_agent_creator import OAIAssistantCreator

import os

dotenv_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '.env'))

config_path = 'src/experiments/groupchat/utils/qa_tool_definition.json'
instruction_path = 'src/experiments/groupchat/utils/qa_instructions.json'
assistant_save_path = "src/data/assistant_id.json"

creator = OAIAssistantCreator(
    dotenv_path, config_path, instruction_path, assistant_save_path, "QualityAssuranceAgent")
creator.run()
