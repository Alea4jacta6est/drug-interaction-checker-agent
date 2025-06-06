import asyncio

from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from agents.mcp.server import MCPServerStdio, MCPServerStreamableHttp

from config import PROMPT_TEMPLATE, MCP_CONFIGS, MODEL_API_KEY


set_tracing_disabled(disabled=True)


async def main(model: str = "mistral/mistral-large-latest"):
    healthcare_server = MCPServerStreamableHttp(
        params=MCP_CONFIGS["healthcare-mcp-public"], name="Healthcare MCP Server"
    )
    mysql_server = MCPServerStdio(
        params=MCP_CONFIGS["mysql"],
            name="MySQL MCP Server"
        )
    whoop_server = MCPServerStdio(params=MCP_CONFIGS["whoop"], name="Whoop MCP Server")

    async with healthcare_server as hserver, mysql_server as mysql, whoop_server as whoop:
        # Create the agent with the connected servers
        agent = Agent(
            name="Assistant",
            instructions=PROMPT_TEMPLATE,
            model=LitellmModel(model=model, api_key=MODEL_API_KEY),
            mcp_servers=[
                hserver,
                whoop,
                mysql
            ],
        )
        # Run the agent with a sample query
        result = await Runner.run(agent, "what are adverse effects of prozac?")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
