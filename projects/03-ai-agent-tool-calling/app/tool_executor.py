# Used to convert the tool arguments (JSON string) into a Python dictionary.
import json

# 'Any' means this parameter can be of any type.
from typing import Any

# Import custom exceptions used for better error handling.
from app.exceptions import (
    ToolExecutionError,
    UnknownToolError,
)

# Import helper function to create a logger for this module.
from app.logging_config import get_logger

# Import the dictionary that maps tool names to Python functions.
from app.tool_registry import TOOL_REGISTRY

# Create a logger named after this module (e.g., app.tool_executor).
logger = get_logger(__name__)


def execute_tool(tool_call: Any) -> dict[str, str]:
    """
    Execute a function requested by the model and return
    a Responses API function-call output.
    """

    # Get the name of the tool requested by the LLM.
    # Example: "calculate"
    tool_name = tool_call.name

    # Look up the actual Python function from the registry.
    # Example:
    # "calculate" -> calculate()
    tool_function = TOOL_REGISTRY.get(tool_name)

    # If the tool name doesn't exist in the registry,
    # raise a custom exception.
    if tool_function is None:
        raise UnknownToolError(f"The requested tool is not registered: {tool_name}")

    try:
        # The model sends tool arguments as a JSON string.
        # Example:
        # '{"expression":"25 * 4"}'
        #
        # json.loads() converts it into a Python dictionary:
        # {"expression": "25 * 4"}
        #
        # If arguments is None or an empty string,
        # use an empty dictionary instead.
        arguments = json.loads(tool_call.arguments or "{}")

        # Write an INFO log before executing the tool.
        logger.info(
            "Executing tool '%s' with arguments %s",
            tool_name,
            arguments,
        )

        # Call the selected function.
        #
        # If arguments is:
        # {"expression": "25 * 4"}
        #
        # this becomes:
        #
        # calculate(expression="25 * 4")
        #
        # The ** operator unpacks dictionary keys into
        # named function arguments.
        result = tool_function(**arguments)

        # Log that execution completed successfully.
        logger.info(
            "Tool '%s' completed successfully",
            tool_name,
        )

    # Catch common execution errors.
    except (TypeError, ValueError, json.JSONDecodeError) as exc:

        # Log the full exception and stack trace.
        logger.exception(
            "Tool '%s' failed",
            tool_name,
        )

        # Raise a custom exception so higher-level code
        # can handle it consistently.
        raise ToolExecutionError(f"Tool '{tool_name}' failed: {exc}") from exc

    # Return the result in the format expected by the
    # OpenAI Responses API.
    return {
        # Indicates this is the output of a function call.
        "type": "function_call_output",
        # Echo back the original call ID so the model knows
        # which tool call this result belongs to.
        "call_id": tool_call.call_id,
        # Convert the result to a string because the API
        # expects text output.
        "output": str(result),
    }
