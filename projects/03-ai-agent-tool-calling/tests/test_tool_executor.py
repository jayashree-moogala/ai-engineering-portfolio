# SimpleNamespace lets us create a lightweight object
# with attributes such as:
#
# tool_call.name
# tool_call.arguments
# tool_call.call_id
#
# It is useful in tests because we don't need to create
# the real OpenAI function-call object.
from types import SimpleNamespace

# Import the pytest testing framework.
import pytest

# Import the custom exception that should be raised
# when an unknown tool is requested.
from app.exceptions import UnknownToolError

# Import the function we want to test.
from app.tool_executor import execute_tool


# -------------------------------------------------------------------
# Test: Calculator Tool
# -------------------------------------------------------------------
#
# Verify that execute_tool() correctly finds
# and executes the calculator tool.
#
def test_execute_calculator_tool() -> None:

    # Create a fake tool-call object.
    #
    # This simulates what the OpenAI Responses API
    # would send when requesting the calculator tool.
    tool_call = SimpleNamespace(
        # Tool selected by the model.
        name="calculate",
        # Tool arguments are always sent as JSON.
        arguments='{"expression": "5 * 6"}',
        # Unique ID assigned by the Responses API.
        call_id="call-123",
    )

    # Execute the requested tool.
    result = execute_tool(tool_call)

    # Verify that execute_tool() returns the exact
    # structure expected by the OpenAI Responses API.
    assert result == {
        # Indicates this object contains a tool result.
        "type": "function_call_output",
        # Must match the original call ID.
        "call_id": "call-123",
        # Calculator result.
        "output": "30",
    }


# -------------------------------------------------------------------
# Test: Date/Time Tool
# -------------------------------------------------------------------
#
# Verify that execute_tool() correctly executes
# the date/time tool.
#
def test_execute_datetime_tool() -> None:

    # Create a fake function call.
    tool_call = SimpleNamespace(
        # Tool selected by the model.
        name="get_current_datetime",
        # This tool takes no parameters,
        # so an empty JSON object is passed.
        arguments="{}",
        # Unique function-call ID.
        call_id="call-456",
    )

    # Execute the tool.
    result = execute_tool(tool_call)

    # Verify the returned object has
    # the expected format.

    assert result["type"] == "function_call_output"

    assert result["call_id"] == "call-456"

    # Verify that some output was returned.
    #
    # We don't check the exact value because
    # the current date and time changes continuously.
    assert result["output"]


# -------------------------------------------------------------------
# Test: Unknown Tool
# -------------------------------------------------------------------
#
# Verify that requesting a tool that does not exist
# raises the correct exception.
#
def test_unknown_tool_raises_error() -> None:

    # Create a fake function call
    # for a tool that is NOT registered.
    tool_call = SimpleNamespace(
        name="missing_tool",
        arguments="{}",
        call_id="call-789",
    )

    # execute_tool() should raise
    # UnknownToolError.
    #
    # If no exception is raised,
    # pytest automatically fails the test.
    with pytest.raises(UnknownToolError):

        execute_tool(tool_call)
