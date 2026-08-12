# Import the os module.
#
# Used here to temporarily set an environment variable
# before importing the application.
import os

# -------------------------------------------------------------------
# Test Environment Setup
# -------------------------------------------------------------------
#
# The OpenAI client requires an API key during startup.
#
# These tests never call OpenAI,
# but app.api creates an Agent during import,
# and that Agent creates an OpenAI client.
#
# To prevent startup failures,
# provide a fake API key.
#
# setdefault() only sets the variable
# if it does not already exist.
#
os.environ.setdefault(
    "OPENAI_API_KEY",
    "test-key",
)

# FastAPI's TestClient simulates HTTP requests
# without starting a real web server.
from fastapi.testclient import TestClient

# Import the FastAPI application
# and the global Agent instance.
from app.api import agent, app

# Create a test client.
#
# The client behaves like a browser or Postman.
#
# Example:
#
# client.get(...)
# client.post(...)
#
client = TestClient(app)


# -------------------------------------------------------------------
# Test: GET /health
# -------------------------------------------------------------------
#
# Verify that the health endpoint
# returns a successful response.
#
def test_health_endpoint() -> None:

    # Simulate:
    #
    # GET /health
    #
    response = client.get("/health")

    # Verify HTTP status.
    assert response.status_code == 200

    # Verify JSON response.
    assert response.json() == {"status": "ok"}


# -------------------------------------------------------------------
# Test: POST /agent
# -------------------------------------------------------------------
#
# Verify that the API correctly calls
# the Agent and returns its response.
#
# Instead of executing the real Agent,
# replace agent.run() with a fake function.
#
def test_agent_endpoint(monkeypatch) -> None:

    # monkeypatch temporarily replaces
    # an object during this test.
    #
    # Replace:
    #
    # agent.run(...)
    #
    # with:
    #
    # lambda message:
    #     "Mock agent response"
    #
    # This prevents:
    #
    # - OpenAI API calls
    # - Tool execution
    # - Conversation memory changes
    #
    monkeypatch.setattr(
        agent,
        "run",
        lambda message: "Mock agent response",
    )

    # Simulate:
    #
    # POST /agent
    #
    # with JSON request body.
    response = client.post(
        "/agent",
        json={"message": "Hello"},
    )

    # Verify successful HTTP response.
    assert response.status_code == 200

    # Verify returned JSON.
    #
    # Since agent.run() was mocked,
    # the answer should always be
    # "Mock agent response".
    assert response.json() == {
        "message": "Hello",
        "answer": "Mock agent response",
    }


# -------------------------------------------------------------------
# Test: Validation
# -------------------------------------------------------------------
#
# Verify that FastAPI/Pydantic rejects
# an empty message.
#
def test_empty_message_is_rejected() -> None:

    # Send an invalid request.
    #
    # The request violates:
    #
    # min_length=1
    #
    # defined in AgentRequest.
    response = client.post(
        "/agent",
        json={"message": ""},
    )

    # FastAPI performs validation BEFORE
    # run_agent() is executed.
    #
    # Therefore the API returns:
    #
    # HTTP 422 Unprocessable Entity
    #
    assert response.status_code == 422
