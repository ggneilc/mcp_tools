import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Obsidian Poster")

@fast.agent(
        "blog_manager",
        instruction="You are a blog management assistant. Use the tools to interact with and create blog posts.",
        servers=["mcp_blog"]
)
@fast.agent(
    "file_manager",
    instruction="You are in charge of a priority data source. Use the tools provided to retrieve context and format answers.",
    servers=["mcp_files"],
)
@fast.agent(
    "email_manager",
    instruction="You are an email management assistant. Use the tools provided to manage emails.",
    servers=["mcp_email"]
)

async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
