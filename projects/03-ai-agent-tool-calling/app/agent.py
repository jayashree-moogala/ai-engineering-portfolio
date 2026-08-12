# Import application settings (loaded from the .env file).
from app.config import settings

# Import custom exceptions used by the Agent.
from app.exceptions import (
    AgentMaxIterationsError,
    InvalidAgentRequestError,
)

# Import logging helper.
from app.logging_config import get_logger

# Import conversation memory.
from app.memory import ConversationMemory

# Import the Planner that communicates with the LLM.
from app.planner import Planner

# Import the function that executes requested tools.
from app.tool_executor import execute_tool

# Create a logger for this module.
logger = get_logger(__name__)


class Agent:
    """
    Main AI Agent.

    Responsibilities:

    - Store conversation history
    - Send requests to the LLM
    - Execute requested tools
    - Continue reasoning until a final answer is produced
    """

    def __init__(
        self,
        planner: Planner | None = None,
        memory: ConversationMemory | None = None,
    ) -> None:
        """
        Constructor.

        Allows dependency injection.

        If no Planner or Memory is provided,
        create default ones.
        """

        # Use the supplied Planner or create one.
        self.planner = planner or Planner()

        # Use the supplied Memory or create one.
        self.memory = memory or ConversationMemory()

    def run(self, user_message: str) -> str:
        """
        Main execution loop.

        This method keeps interacting with the model until:

        1. A final answer is produced

        OR

        2. The maximum number of tool iterations is reached.
        """

        # Remove leading and trailing whitespace.
        cleaned_message = user_message.strip()

        # Reject empty questions.
        if not cleaned_message:
            raise InvalidAgentRequestError("The user message cannot be empty.")

        # Log that a new request has started.
        logger.info("Agent received a new request")

        # Save the user's message into conversation memory.
        self.memory.add_user_message(cleaned_message)

        # Ask the model what it wants to do.
        #
        # The model may:
        #
        # - answer directly
        #
        # OR
        #
        # - request one or more tool calls.
        response = self.planner.plan(self.memory.get_messages())

        # Main reasoning loop.
        #
        # The agent may perform multiple tool calls before
        # producing the final answer.
        for iteration in range(
            1,
            settings.agent_max_iterations + 1,
        ):

            logger.info(
                "Agent iteration %s",
                iteration,
            )

            # Extract all function calls returned by the model.
            #
            # response.output contains many output items.
            #
            # Keep only those whose type is "function_call".
            tool_calls = [
                item for item in response.output if item.type == "function_call"
            ]

            # If there are NO tool calls,
            # the model has finished reasoning.
            if not tool_calls:

                # Get the final text answer.
                final_answer = response.output_text.strip()

                # Save the assistant's response into memory.
                self.memory.add_assistant_message(final_answer)

                logger.info("Agent produced a final answer")

                # Return the completed answer.
                return final_answer

            # Store outputs from every executed tool.
            tool_outputs = []

            # Execute every requested tool.
            #
            # Some models may request multiple tools
            # in a single response.
            for tool_call in tool_calls:

                logger.info(
                    "Model selected tool '%s'",
                    tool_call.name,
                )

                # Execute the Python function and collect
                # its output.
                tool_outputs.append(execute_tool(tool_call))

            # Send all tool outputs back to the model.
            #
            # The model continues reasoning using
            # the tool results.
            response = self.planner.continue_with_tool_outputs(
                previous_response_id=response.id,
                tool_outputs=tool_outputs,
            )

        # If the loop finishes,
        # the model never produced a final answer.
        raise AgentMaxIterationsError(
            "The agent reached the maximum number of " "tool-execution iterations."
        )

    def clear_memory(self) -> None:
        """
        Remove all stored conversation history.
        """

        self.memory.clear()

        logger.info("Conversation memory cleared")
