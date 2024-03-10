import json
from src.create_oai_agent.ToolDefinitionFactory import ToolDefinitionFactory

config_path = 'src/create_oai_agent/tool_definitions/tool_definitions.json'

factory = ToolDefinitionFactory(config_path)

tool = []
for tool_type in factory.config:
    tool.append(factory.create_tool_definition(tool_type))

# print it using json
print(json.dumps(tool, indent=4))
