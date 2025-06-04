import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

from drug_tools.drug_info_tool import (
    get_drug_indications,
    get_drug_adverse_effects,
    get_negative_effects,
)
from drug_tools.drug_interaction_tool import (
    get_positive_interactions,
    get_negative_interactions,
)

from prompts.drug_prompts import drug_assistant_prompt

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
        name="Drug Assistant",
        instructions=drug_assistant_prompt,
        model=LitellmModel(model=model, api_key=api_key),
        #tools=[DrugInformationTool.query_drug_data],
        tools=[
            get_drug_indications,
            get_drug_adverse_effects,
            get_negative_effects,
            get_positive_interactions,
            get_negative_interactions
        ],
    )

    test_queries = [
        "What are the indications for acebutolol?",
        "What are the adverse effects for acebutolol?",
        "Can tamoxifen cause somnolence?",
        "Is acebutolol prescribed for crohn's disease?",
        "Is acebutolol used for hypertension?",
        "Is there a known interaction between timolol and sunitinib",
        "Is there a known interaction between desmopressin and clopamide",
    ]

    for query in test_queries:
        result = await Runner.run(agent, query)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())