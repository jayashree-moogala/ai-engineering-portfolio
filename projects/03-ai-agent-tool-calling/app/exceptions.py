# provide meaningful errors instead of generic ValueError exceptions


class AgentError(Exception):
    """Base exception for agent-related failures."""


class InvalidAgentRequestError(AgentError):
    """Raised when the user request is empty or invalid."""


class UnknownToolError(AgentError):
    """Raised when the model requests an unregistered tool."""


class ToolExecutionError(AgentError):
    """Raised when a registered tool fails during execution."""


class AgentMaxIterationsError(AgentError):
    """Raised when the agent cannot finish within its iteration limit."""
