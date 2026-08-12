import json

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.tools.calculator import calculate
from app.tools.tool_definitions import CALCULATOR_TOOL


class Agent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def run(self, user_message: str) -> str:
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            input=user_message,
            tools=[CALCULATOR_TOOL],
        )

        tool_outputs = []

        for item in response.output:
            if item.type == "function_call" and item.name == "calculate":
                arguments = json.loads(item.arguments)

                result = calculate(arguments["expression"])

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(result),
                    }
                )

        if not tool_outputs:
            return response.output_text

        final_response = self.client.responses.create(
            model=OPENAI_MODEL,
            previous_response_id=response.id,
            input=tool_outputs,
            tools=[CALCULATOR_TOOL],
        )

        return final_response.output_text