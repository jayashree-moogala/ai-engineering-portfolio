# Agent basic conversation history
from dataclasses import dataclass, field


@dataclass
class ConversationMemory:
    """
    Stores conversation messages for one agent instance.

    This is in-memory storage only. It is cleared when the
    application restarts.
    """

    # list of dictionary(key/value pair). Create a new empty list for every new object
    messages: list[dict[str, str]] = field(default_factory=list)
    max_messages: int = 20

    def add_user_message(self, content: str) -> None:
        self.messages.append(
            {
                "role": "user",
                "content": content,
            }
        )
        self._trim()

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(
            {
                "role": "assistant",
                "content": content,
            }
        )
        # discards more than <max_messages> messages ( oldest ones are discarded )
        self._trim()

    def get_messages(self) -> list[dict[str, str]]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()

    def _trim(self) -> None:
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]
