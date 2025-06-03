import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel


set_tracing_disabled(disabled=True)


@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


# anthropic/claude-3-5-sonnet-20240620
async def main(api_key: str, model: str = "mistral/mistral-large-latest"):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus about a sunny weather.",
        model=LitellmModel(model=model, api_key=api_key),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Paris?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())