import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Obsidian Poster")

# Define the agent
@fast.agent(
    "blog_manager",
    instruction=" \
    You are a blog management assistant. \
    You will receive HTML content from the file manager. \
    Create a new blog post using this content. \
    Extract a suitable title from the content and use appropriate tags.",
    servers=["mcp_blog"]
)
@fast.agent(
    "file_manager",
    instruction=" \
    You are a knowledge retrieval assistant with access to a vector database of documents. \
    When given a query/topic, use the create_blog_content tool with the topic(s) as a list. \
    This tool will retrieve relevant documents, clean them up, and format them as HTML. \
    Return only the HTML content from this tool to the blog manager. \
    Do NOT call multiple tools or dump raw database content.",
    servers=["mcp_files"]
)
@fast.chain(
    name="doc_to_post",
    sequence=["file_manager", "blog_manager"],
)

async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        query = "Create a blog post about Vectors from the documents in the database."
        await agent.doc_to_post(query)


if __name__ == "__main__":
    asyncio.run(main())
