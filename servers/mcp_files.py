"""
MCP server for mock RAG for Obsidian vault.
# Tools
- create_blog_content: creates a blog post on a given topic from an obsidian note
- answer_question: provides answers to questions based on the content of obsidian notes

Methods:
- get_context: retrieves relevant documents from the vector database based on a query
- markdown_to_html: converts Markdown content to HTML format
"""
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent, SamplingMessage
import pickle, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from typing import List, Optional
import markdown2

# Create an MCP server
mcp = FastMCP("Obsidian Note Indexer", version="0.1.0")

# — Load FAISS + metadata —
idx    = faiss.read_index(r"C:\Users\nchur\Documents\machine-learning\ollama-obsidian\rag\docs_index.faiss")
with open(r"C:\Users\nchur\Documents\machine-learning\ollama-obsidian\rag\docs_metadata.pkl", "rb") as f:
    chunks = pickle.load(f)

# — Embedder reused for queries —
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(query: str, k: int = 5):
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    _, ids = idx.search(q_emb, k)
    return [chunks[i] for i in ids[0]]

# — MCP Tools and Prompts —

@mcp.tool(title="Create Blog Content")
def create_blog_content(topic: List[str]) -> str:
    """Create a blog post on a given topic from an obsidian note."""
    context = get_context(topic)
    # Here you would typically call a model to generate the blog content
    return f"Blog post for {topic}:\n\n{context}"

@mcp.tool(title="Summarize Information")
async def summarize_information(topics: List[str], ctx: Context) -> str:
    """Summarize information based on the retrieved content."""
    try:
        # Get initial context on the topics
        context = get_context(topics)
        # Create a simple prompt for additional topics
        prompt = f"Based on this context about {topics}, suggest 2-3 related topics (comma-separated):\n\n{context}..."
        # Sample to get additional topics with proper message structure
        result = await ctx.session.create_message(
            messages=[
                SamplingMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt)
                )
            ],
            max_tokens=100,
        )
        content_text = result.content.text if hasattr(result.content, 'text') else str(result.content)
        new_topics = [t.strip() for t in content_text.split(",") if t.strip()]
        additional_context = get_context(new_topics)
        context += f"\n\n## Additional Context:\n{additional_context}"
        return f"Context for {topics+new_topics}:\n\n{context}\n\n Summarized Answer:"
    except Exception as e:
        # Fallback to just the initial context if sampling fails
        context = get_context(topics)
        return f"Context for {topics}:\n\n{context}\n\n(Note: Could not expand topics due to: {str(e)})"

# - Helper tools/functions -
@mcp.tool(title="Find Relevant Documents")
def get_context(topics: List[str]) -> str:
    """Utilize the vector database to retrieve relevant chunks to answer a query."""
    full_context = f"CONTEXT FOR TOPIC(s): {topics}"
    for t in topics:
        hits = retrieve(t, k=5)
        # Merge top‑k chunks into context
        context = "\n\n".join(f"[{h['source']}#{h['idx']}]\n{h['text']}" for h in hits)
        full_context += f"## Context for TOPIC: {t}\n\n{context}\n\n"

    return full_context

@mcp.tool(title="Markdown to HTML")
def markdown_to_html(markdown_input: TextContent ) -> str:
    """Convert the response content of a file from Markdown to HTML."""
    html_content = markdown2.markdown(markdown_input.content.text)
    # Ensure the HTML is well-formed
    html_content = html_content.replace("\n", "<br>").replace('"', '\\"')
    html_content = f"<html><body>{html_content}</body></html>"
    return html_content

@mcp.prompt(title="Knowledge Base Prompt")
def knowledge_base_prompt(prompt: str) -> str:
    """Return a system prompt based on the context from the vector database."""
    system_prompt = f" \
        You are in charge of all the documents in an Obsidian vault, which is a personal knowledge management system. \
        You have access to a vector database that contains embeddings of all the documents. \
        Only utilize the information in the Obsidian vault to answer the question. \
        Respond in a concise manner, using the information provided in the context. \
        As you receive more context, update your queries and use check_database again until you have a complete answer. \
        Topic: {prompt}"
    return system_prompt

@mcp.prompt(title="Summarize Information Prompt")
def summarize_information_prompt(prompt: str) -> str:
    """Return a system prompt for summarizing information."""
    system_prompt = f" \
        Summarize the information from the context given by the tool `summarize_information` \
        To give a concise summary of the key points about the topic, \
        Use the Topic: '{prompt}' as the parameter for `summarize_information`."
    return system_prompt

def main():
    """Entry point for the direct execution server."""
    mcp.run()


if __name__ == "__main__":
    main()