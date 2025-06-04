import os
import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

#from drug_tools.drug_info_tool import DrugInformationTool
from drug_tools.drug_info_tool import get_drug_indications, get_drug_adverse_effects, get_negative_effects
from drug_tools.drug_interaction_tool import get_positive_interactions, get_negative_interactions

from dotenv import load_dotenv
load_dotenv()

mistral_api_key = os.getenv("MISTRAL_API_KEY")
claude_api_key = os.getenv("CLAUDE_API_KEY")


set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


# anthropic/claude-3-5-sonnet-20240620
async def main(api_key: str = mistral_api_key, model: str = "mistral/mistral-large-latest"):
    agent = Agent(
        name="Assistant",
        instructions="""
            From user input, identify:
            1. Mentioned drug(s).
            2. Whether the user is asking about indications, adverse effects, or interactions.

            Use the available tools to retrieve and summarize relevant data. If results are extensive, highlight the most critical information (e.g., severe or common effects). Do not describe tables or internal tool structure. Do not infer unknown connections. Clearly state when no known information exists. Use both positive and negative tools when asked about adverse effects and interactions.
            """,
        model=LitellmModel(model=model, api_key=api_key),
        #tools=[DrugInformationTool.query_drug_data],
        tools=[get_drug_indications, get_drug_adverse_effects, get_negative_effects, get_positive_interactions, get_negative_interactions],
    )

    result = await Runner.run(agent, "What are the indications for acebutolol?")
    print(result.final_output)

    result = await Runner.run(agent, "What are the adverse effects for acebutolol?")
    print(result.final_output)

    result = await Runner.run(agent, "Can tamoxifen cause somnolence?")
    print(result.final_output)

    result = await Runner.run(agent, "Is acebutolol prescribed for crohn's disease?")
    print(result.final_output)

    result = await Runner.run(agent, "Is acebutolol used for hypertension?")
    print(result.final_output)

    result = await Runner.run(agent, "Is there a known interaction between timolol and sunitinib")
    print(result.final_output)

    result = await Runner.run(agent, "Is there a known interaction between desmopressin and clopamide")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())