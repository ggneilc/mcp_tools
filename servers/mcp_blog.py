"""
MCP server for managing blog posts.
- Resource : blog posts in a SQL database.
- Tool : list_posts, get_post, create_post
"""
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import TypedDict, List
import requests

SERVER_URL = "http://localhost:5000"

mcp = FastMCP("Blog Server", version="0.1.0")

class BlogPost(BaseModel):
    id: int
    content: str = Field(description="The HTML string of the blog post's content.")
    title: str = Field(description="The title of the blog post.")
    tags: List[str] = Field(description="Comma-separated tags for the blog post.")


@mcp.tool()
def list_posts() -> List[BlogPost]:
    """List all blog posts."""
    response = requests.get(f"{SERVER_URL}/posts")
    if response.status_code == 200:
        response = response.json()
        return [BlogPost(**post) for post in response]
    return []

@mcp.tool()
def get_post(post_id: int) -> BlogPost:
    """Get a specific blog post by ID."""
    response = requests.get(f"{SERVER_URL}/posts/{post_id}")
    if response.status_code == 200:
        return response.json()
    return "Error fetching post."

@mcp.tool()
def create_post(title: str, content: str, tags: str) -> str:
    """Create a new blog post."""
    response = requests.post(f"{SERVER_URL}/posts", json={
        "title": title,
        "content": content,
        "tags": tags
    })
    if response.status_code == 201:
        return success_message()
    return "Error creating post."

@mcp.tool()
def delete_post(post_id: int) -> str:
    """Delete a blog post by ID."""
    response = requests.delete(f"{SERVER_URL}/posts/{post_id}")
    if response.status_code == 204:
        return success_message()
    return "Error deleting post."

@mcp.prompt("Success")
def success_message() -> str:
    """Return a success message."""
    prompt = """
    The tool use was successful.
    Respond to the user with 1 word: 'Done'.
    """
    return prompt.strip()


def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":
    main()