from typing import Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


def create_tool_definition(name: str,
                           description: str,
                           parameters: Optional[Dict[str, Dict[str, Union[str, bool]]]] = None) -> Dict:
    """
    Create a tool definition for the given function name, description and parameters.

    Args:
    - name: Name of the function
    - description: Description of the function
    - parameters: Parameters of the function

    Returns:
    - tool_definition: Tool definition for the function
    """

    tool_definition = {
        "function": {
            "name": name,
            "description": description,
            "parameters": {}
        }
    }

    if parameters is not None:
        tool_definition["function"]["parameters"] = {
            "properties": {},
            "required": [],
            "type": "object"
        }

        for param_name, param_info in parameters.items():
            tool_definition["function"]["parameters"]["properties"][param_name] = param_info
            if 'required' in param_info and param_info['required']:
                tool_definition["function"]["parameters"]["required"].append(
                    param_name)

    return tool_definition
