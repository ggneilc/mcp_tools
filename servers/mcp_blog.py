"""
MCP server for managing blog posts.
- Resource : blog posts in a SQL database.
- Tool : list_posts, get_post, create_post
"""
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field
from typing import TypedDict, List
import requests
import markdown2

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
def list_keyword_post_ids(query: str) -> List[int]:
    """
    Check all blog post titles for a specific keyword 
    @param: query - keyword to search
    @return: list of all post ids with query in title, -1 indicates keyword not found
    """
    response = requests.get(f"{SERVER_URL}/posts")
    posts = [BlogPost(**post) for post in response.json()]
    return [int(post.id) if (query in post.title.lower()) else -1 for post in posts]

@mcp.tool()
async def create_post(title: str, content: str, tags: List[str], ctx: Context) -> str:
    """
    Create a new blog post.
    @param: title - post title string
    @param: content - body of post, formatted in markdown
    @param: tags - list of strings that represent topic area
    @return - success/failure message
    """
    extras = ["fenced-code-blocks", "tables", "strike", "cuddled-list"]
    html = markdown2.markdown(content, extras=extras)
#    html = html.replace("\n", "<br>").replace('"', '\\"')
    await ctx.info(content)
    await ctx.info(html)
    response = requests.post(f"{SERVER_URL}/posts", json={
        "title": title,
        "content": html,
        "tags": ",".join(tags)
    })
    if response.status_code == 201:
        return "Successfully created post. Do not call this tool again. You have completed your task."
    return "Error creating post."

@mcp.tool()
def delete_posts(post_id: int) -> str:
    """Delete a blog post by ID."""
    response = requests.delete(f"{SERVER_URL}/posts/{post_id}")
    if response.status_code == 204:
        return "Success"
    return "Error deleting post."


def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":
    main()
