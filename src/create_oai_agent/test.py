from src.create_oai_agent.tool_definition import create_tool_definition
from src.create_oai_agent.tool_parameters import tool_parameters

import json

tool_definition = create_tool_definition(
    name="input_text",
    description="Interacts with a webpage by sending keys to input fields based on a provided query, and returns a response string with the result of the action or an error message. The process includes highlighting input elements, taking a screenshot for analysis, and then processing the inputs as per the query.",
    parameters={
        "properties": tool_parameters["input_text"],
        "required": ["query"],
        "type": "object"
    }
)

print(json.dumps(tool_definition, indent=4))
