from typing import Any  # 'Any' means the function may return any type.

# Import the OpenAI client used to communicate with the Responses API.
from openai import OpenAI

# Import application settings loaded from the .env file.
from app.config import settings

# Import the list of tool definitions that will be sent to the model.
from app.tools.tool_definitions import AVAILABLE_TOOLS

# This is the system prompt (instructions) given to the model
# before every conversation.
#
# It defines the assistant's behavior and tells the model
# when it should use tools.
SYSTEM_PROMPT = """
You are a helpful AI assistant with access to tools.

Rules:
1. Use the calculate tool for arithmetic.
2. Use get_current_datetime for current date or time.
3. Never guess current information that a tool can provide.
4. You may call multiple tools when necessary.
5. Use tool results to produce a clear final answer.
"""


class Planner:
    """
    The Planner is responsible for communicating with the LLM.

    It sends:
      - conversation history
      - available tools
      - system instructions

    and receives:

      - either a final answer
      - or one/more tool calls
    """

    def __init__(self) -> None:
        """
        Constructor.

        Runs once when a Planner object is created.
        """

        # Create an OpenAI client using the API key
        # stored in the .env file.
        self.client = OpenAI(api_key=settings.openai_api_key)

        # Store the model name.
        #
        # Example:
        # "gpt-4.1-mini"
        self.model = settings.openai_model

        # Store the list of available tools.
        #
        # This list is sent to the model on every request
        # so the model knows which tools it is allowed to call.
        self.tools = AVAILABLE_TOOLS

    def plan(
        self,
        messages: list[dict[str, str]],
    ) -> Any:
        """
        Send the current conversation to the model.

        The model will either:

        1. Respond directly if no defined tools are used

        or

        2. Request one or more tool calls.
        """

        # Call the OpenAI Responses API.
        return self.client.responses.create(
            # Which model should answer?
            model=self.model,
            # System instructions that guide the model.
            instructions=SYSTEM_PROMPT,
            # Conversation history.
            #
            # Example:
            #
            # [
            #   {
            #     "role":"user",
            #     "content":"What is 25 * 4?"
            #   }
            # ]
            input=messages,
            # List of available tools.
            #
            # The model reads these tool definitions
            # and decides whether to call one.
            tools=self.tools,
        )

    def continue_with_tool_outputs(
        self,
        previous_response_id: str,
        tool_outputs: list[dict[str, str]],
    ) -> Any:
        """
        Continue a previous model response after one or
        more tools have been executed.

        The model receives:

        - the tool results
        - the previous response ID

        and generates the final answer.
        """

        # Continue the existing conversation.
        #
        # The previous_response_id tells OpenAI:
        #
        # "Continue thinking from the previous response
        # instead of starting a brand-new conversation."
        return self.client.responses.create(
            # Same model as before.
            model=self.model,
            # Continue the previous response.
            previous_response_id=previous_response_id,
            # Tool outputs.
            #
            # Example:
            #
            # [
            #   {
            #     "type": "function_call_output",
            #     "call_id": "...",
            #     "output": "100"
            #   }
            # ]
            input=tool_outputs,
            # Send the tools again.
            #
            # This allows the model to decide whether
            # another tool call is required.
            #
            # Example:
            #
            # User:
            # "What's today's date and how many days
            # until Christmas?"
            #
            # Tool 1:
            # get_current_datetime()
            #
            # Model may decide it has enough information,
            # or it may call another tool.
            tools=self.tools,
        )
