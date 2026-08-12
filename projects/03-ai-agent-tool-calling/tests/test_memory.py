# Import the ConversationMemory class that we want to test.
from app.memory import ConversationMemory


# -------------------------------------------------------------------
# Test: Messages are stored correctly
# -------------------------------------------------------------------
#
# Verify that both user and assistant messages
# are stored in the correct order.
#
def test_memory_stores_messages() -> None:

    # Create a new, empty conversation memory.
    memory = ConversationMemory()

    # Add a user message.
    memory.add_user_message("Hello")

    # Add the assistant's reply.
    memory.add_assistant_message("Hi")

    # Verify that the conversation history
    # exactly matches what we expect.
    assert memory.get_messages() == [
        # First message should be from the user.
        {
            "role": "user",
            "content": "Hello",
        },
        # Second message should be from the assistant.
        {
            "role": "assistant",
            "content": "Hi",
        },
    ]


# -------------------------------------------------------------------
# Test: Conversation can be cleared
# -------------------------------------------------------------------
#
# Verify that calling clear() removes
# every stored message.
#
def test_memory_can_be_cleared() -> None:

    # Create a new memory object.
    memory = ConversationMemory()

    # Store one message.
    memory.add_user_message("Hello")

    # Remove all stored messages.
    memory.clear()

    # The conversation history should now be empty.
    assert memory.get_messages() == []


# -------------------------------------------------------------------
# Test: Old messages are trimmed
# -------------------------------------------------------------------
#
# Verify that ConversationMemory keeps only
# the most recent messages when the maximum
# capacity is exceeded.
#
def test_memory_trims_old_messages() -> None:

    # Create memory that can hold only
    # two messages.
    memory = ConversationMemory(max_messages=2)

    # Add first message.
    memory.add_user_message("One")

    # Add second message.
    memory.add_assistant_message("Two")

    # Add third message.
    #
    # Since max_messages = 2,
    # the oldest message ("One")
    # should be removed automatically.
    memory.add_user_message("Three")

    # Verify that only two messages remain.
    assert len(memory.get_messages()) == 2

    # Verify that the oldest remaining message
    # is now "Two".
    #
    # The expected conversation is:
    #
    # Assistant: Two
    # User: Three
    #
    assert memory.get_messages()[0]["content"] == "Two"
