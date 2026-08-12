from collections.abc import Callable
from typing import Any

from app.tools.calculator import calculate
from app.tools.date_time import get_current_datetime

# Type alias - A function that can accept any number of arguments and return any type.
ToolFunction = Callable[..., Any]

# Dictionary stores tool functions
TOOL_REGISTRY: dict[str, ToolFunction] = {
    "calculate": calculate,
    "get_current_datetime": get_current_datetime,
}
