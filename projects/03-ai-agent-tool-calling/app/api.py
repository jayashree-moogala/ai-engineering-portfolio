# Import FastAPI framework used to build REST APIs.
# HTTPException is used to return HTTP error responses
# such as 400 or 500.
from fastapi import FastAPI, HTTPException

# Pydantic is used to define request and response models.
# It automatically validates incoming JSON.
from pydantic import BaseModel, Field

# Import the AI Agent.
from app.agent import Agent

# Import the application's custom exception hierarchy.
from app.exceptions import AgentError

# Import logging helpers.
from app.logging_config import (
    configure_logging,
    get_logger,
)

# Configure logging once when the application starts.
configure_logging()

# Create a logger for this module.
logger = get_logger(__name__)

# Create the FastAPI application.
#
# These values appear in:
#
# http://localhost:8000/docs
#
app = FastAPI(
    title="AI Agent with Tool Calling",
    version="1.0.0",
)

# Create one Agent instance.
#
# Every incoming request uses this same agent.
agent = Agent()


# -----------------------------
# Request Model
# -----------------------------
#
# Defines the JSON format expected by POST /agent.
#
# Example request:
#
# {
#   "message": "What is 25 * 4?"
# }
#
class AgentRequest(BaseModel):

    # Required field.
    #
    # Field(...) means the field is mandatory.
    #
    # min_length and max_length provide automatic
    # validation before the request reaches the Agent.
    message: str = Field(
        ...,
        min_length=1,
        max_length=4_000,
        description="Message to send to the AI agent.",
    )


# -----------------------------
# Response Model
# -----------------------------
#
# Defines the JSON returned by POST /agent.
#
# Example:
#
# {
#   "message": "What is 25 * 4?",
#   "answer": "25 * 4 = 100"
# }
#
class AgentResponse(BaseModel):
    message: str
    answer: str


# -----------------------------
# Health Check Response
# -----------------------------
#
# Returned by GET /health.
#
class HealthResponse(BaseModel):
    status: str


# -----------------------------
# GET /health
# -----------------------------
#
# Simple endpoint used by monitoring tools
# to verify that the API is running.
#
@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:

    # Return a simple success response.
    return HealthResponse(status="ok")


# -----------------------------
# POST /agent
# -----------------------------
#
# Main endpoint.
#
# Receives a user's message,
# runs the AI Agent,
# and returns the answer.
#
@app.post(
    "/agent",
    response_model=AgentResponse,
)
def run_agent(
    request: AgentRequest,
) -> AgentResponse:

    try:

        # Run the AI Agent.
        #
        # This may involve:
        #
        # - LLM reasoning
        # - Tool execution
        # - Multiple iterations
        answer = agent.run(request.message)

        # Return the response as JSON.
        return AgentResponse(
            # Echo the original message.
            message=request.message,
            # Final answer produced by the agent.
            answer=answer,
        )

    # Handle expected agent errors.
    #
    # Examples:
    #
    # - Empty request
    # - Unknown tool
    # - Tool execution failure
    except AgentError as exc:

        logger.warning(
            "Agent request failed: %s",
            exc,
        )

        # Return HTTP 400 (Bad Request).
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    # Handle unexpected programming errors.
    except Exception as exc:

        # Log the complete stack trace.
        logger.exception("Unexpected agent failure")

        # Return HTTP 500 (Internal Server Error).
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred.",
        ) from exc


# -----------------------------
# DELETE /memory
# -----------------------------
#
# Clears the conversation history stored
# inside the Agent.
#
@app.delete("/memory")
def clear_memory() -> dict[str, str]:

    # Reset conversation memory.
    agent.clear_memory()

    # Return confirmation.
    return {"status": "conversation memory cleared"}
