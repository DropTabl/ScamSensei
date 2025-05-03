import asyncio
import dspy
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from backend.url_checking.url_checking_tool import check_url_with_urlscan  # no need for `summary()` now
from backend.utils.helper import init_llm, BASE_URL, MODEL_NAME, API_KEY


# Init model client
model_client = OpenAIChatCompletionClient(
    model=MODEL_NAME,
    api_key=API_KEY,
    base_url=BASE_URL,
    model_capabilities={
        "json_output": True,
        "vision": False,
        "function_calling": True,
        "structured_output": True,
    },
)

# Define the agent
agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[],  # No longer auto-calling the tool — we're calling it manually
    system_message=(
        "You are a helpful assistant that interprets results from URL safety checks."
    ),
)


class Interpreter(dspy.Signature):
    """Explain in natural language whether the URL is safe or not, based on results from a safety check."""
    question: str = dspy.InputField(desc="The results from a safety check performed on the URL.")
    answer: str = dspy.OutputField(desc="Explanation of the safety status of the URL.")
    score: int = dspy.OutputField(desc="Risk score from 0 to 10. Higher means riskier.")


# Main function to run a full safety check and explain it
async def main(url: str, language: str = "en"):
    # Run actual safety check tool manually (not via agent)
    result_data, formatted_summary = await check_url_with_urlscan(url)
    if not formatted_summary:
        raise ValueError("No result returned from urlscan.")

    # Ask agent to explain it using DSPy
    qa = dspy.Predict(Interpreter)
    prompt = (
        f"The following is a result from a safety scan of a URL:\n{formatted_summary}\n\n"
        f"Explain in natural language whether it is safe or not, and why. Answer in: {language}"
    )
    interpretation = qa(question=prompt)

    return formatted_summary, interpretation.answer, interpretation.score
