# Define the calculator as an OpenAI tool

# This schema tells the model:
#   the tool’s name
#   when it should be used
#   what argument it accepts
#   the required JSON structure

# the tool schema matches the function signature - name and parameters
CALCULATOR_TOOL = {
    "type": "function",
    "name": "calculate",
    "description": (
        "Use this tool for arithmetic calculations. "
        "Provide the complete arithmetic expression as a string."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": ("Arithmetic expression, such as " "'(125 * 8) + 45'."),
            }
        },
        "required": ["expression"],
        "additionalProperties": False,
    },
    "strict": True,
}


CURRENT_DATETIME_TOOL = {
    "type": "function",
    "name": "get_current_datetime",
    "description": (  # tool prompting
        "Use this tool whenever the user asks for the "
        "current date, current time, today's date, "
        "current timestamp, or local date and time. "
        "Never guess the current date or time."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
    "strict": True,
}


AVAILABLE_TOOLS = [
    CALCULATOR_TOOL,
    CURRENT_DATETIME_TOOL,
]
