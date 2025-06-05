import os
import asyncio
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents.mcp.server import MCPServerStdio, MCPServerStreamableHttp, MCPServerSse

from drug_tools.drug_info_tool import (
    get_drug_indications,
    get_drug_adverse_effects,
    get_negative_effects,
)
from drug_tools.drug_interaction_tool import (
    get_positive_interactions,
    get_negative_interactions,
)

from prompts.drug_prompts import drug_tools_prompt, drug_mcp_prompt

load_dotenv()

mistral_api_key = os.getenv("MISTRAL_API_KEY")
claude_api_key = os.getenv("CLAUDE_API_KEY")


set_tracing_disabled(disabled=True)


mysql_server = MCPServerStdio(
    params={
            "command": os.getenv("MYSQL_MCP_COMMAND"),
            "args": [os.getenv("MYSQL_MCP_ARGS")],
            "cwd": os.getenv("MYSQL_MCP_CWD"),
        },
        name="Healthcare MCP Server"
    )


# anthropic/claude-3-5-sonnet-20240620
async def main_tools(api_key: str = os.getenv("MISTRAL_API_KEY"), model: str = "mistral/mistral-large-latest"):
    agent = Agent(
        name="Drug Assistant",
        instructions=drug_tools_prompt,
        model=LitellmModel(model=model, api_key=api_key),
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


async def main_mcp(api_key: str = os.getenv("MISTRAL_API_KEY"), model: str = "mistral/mistral-large-latest"):
    async with mysql_server as mysql:
            # Create the agent with the connected servers
            agent = Agent(
                name="Assistant",
                instructions=drug_mcp_prompt,
                model=LitellmModel(model=model, api_key=api_key),
                mcp_servers=[mysql],  # pass the live server connections here
            )
            print('OBJECT', agent)
            # Run the agent with a sample query
            result = await Runner.run(agent, "Can I take desmopressin and clopamide together?")
            print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main_mcp())