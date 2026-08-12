# SimpleNamespace lets us quickly create lightweight
# objects with attributes.
#
# Here it is used to simulate an OpenAI Responses API
# response without calling the real API.
from types import SimpleNamespace

# Import the Agent class we want to test.
from app.agent import Agent

# Import the real ConversationMemory.
from app.memory import ConversationMemory


# -------------------------------------------------------------------
# Fake Planner
# -------------------------------------------------------------------
#
# This class replaces the real Planner during testing.
#
# Instead of calling OpenAI, it returns a predefined response.
#
class FakePlanner:

    def __init__(self) -> None:

        # Used to verify that the Agent actually
        # called Planner.plan().
        self.plan_called = False

    def plan(self, messages):

        # Record that this method was invoked.
        self.plan_called = True

        # Simulate a Responses API object.
        #
        # output = []
        #
        # means:
        #
        # "The model requested NO tool calls."
        #
        # output_text contains the final answer.
        return SimpleNamespace(
            # Fake response ID.
            id="response-1",
            # Empty output means
            # no function calls.
            output=[],
            # Final answer produced by the fake model.
            output_text="This is the final answer.",
        )

    def continue_with_tool_outputs(
        self,
        previous_response_id,
        tool_outputs,
    ):
        """
        This method should NEVER be called
        during this test.

        Since the fake model returned a final answer
        immediately, the Agent should not attempt
        another planning step.
        """

        raise AssertionError("No tool continuation was expected.")


# -------------------------------------------------------------------
# Test: Agent returns a direct answer
# -------------------------------------------------------------------
#
# Verify that when the model immediately returns
# an answer (without requesting tools),
# the Agent:
#
# 1. Calls Planner.plan()
# 2. Returns the answer
# 3. Stores the answer in memory
#
def test_agent_returns_direct_answer() -> None:

    # Create the fake planner.
    planner = FakePlanner()

    # Create real conversation memory.
    memory = ConversationMemory()

    # Create an Agent using the fake planner.
    #
    # This is called dependency injection.
    #
    # The Agent behaves normally,
    # but no real API calls are made.
    agent = Agent(
        planner=planner,
        memory=memory,
    )

    # Execute the Agent.
    answer = agent.run("Explain prompt engineering.")

    # Verify that Planner.plan() was called.
    assert planner.plan_called is True

    # Verify that the returned answer matches
    # what the fake planner produced.
    assert answer == "This is the final answer."

    # Verify that the assistant's response
    # was stored in conversation memory.
    assert memory.get_messages()[-1] == {
        # Last message should belong
        # to the assistant.
        "role": "assistant",
        # And should contain the final answer.
        "content": "This is the final answer.",
    }
