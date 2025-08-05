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
import re

SERVER_URL = "http://localhost:5000"

mcp = FastMCP("Blog Server", version="0.1.0")

class BlogPost(BaseModel):
    id: int = Field(description="Primary Key of the BlogPost.")
    content: str = Field(description="The HTML string of the blog post's content.")
    title: str = Field(description="The title of the blog post.")
    tags: List[str] = Field(description="Comma-separated tags for the blog post.")


@mcp.tool()
def list_posts() -> List[BlogPost]:
    """
    List all blog posts.
    @param: None
    @return - List of each BlogPost
    """
    response = requests.get(f"{SERVER_URL}/posts")
    if response.status_code == 200:
        response = response.json()
        return [BlogPost(**post) for post in response]
    return []

@mcp.tool()
def get_post(post_id: int) -> BlogPost:
    """
    Get a specific blog post by ID.
    @param: post_id - the primary key of the BlogPost
    @return - json of BlogPost
    """
    response = requests.get(f"{SERVER_URL}/posts/{post_id}")
    if response.status_code == 200:
        return response.json()
    return "Error fetching post."

@mcp.tool()
def get_most_recent_post_id() -> int:
    """
    Returns the ID of the most recently created BlogPost
    @param: None
    @return - id or failure message
    """
    response = requests.get(f"{SERVER_URL}/posts")
    if response.ok:
        response = response.json()
        key, post = response.popitem()  # pops the last inserted pair
        return f"The most recent BlogPost id = {post.id}"
    return "Error fetching post."

@mcp.tool()
def update_post(
        id: int, 
        title: str | None = None,
        content: str | None = None,
        tags: List[str] | None = None
    ) -> str:
    """
    Update a specific BlogPost.
    @param: id - BlogPost to be updated
    @param: title - OPTIONAL; new title for the BlogPost
    @param: content - OPTIONAL; new content for the BlogPost
    @param: tags - OPTIONAL; new tag list for the BlogPost
    @return - success/failure message 
    """
    response = requests.get(f"{SERVER_URL}/posts/{id}")
    if response.ok:
        response = requests.put(f"{SERVER_URL}/posts/{id}", json={
            "title": title,
            "content": content,
            "tags": tags
        })
        if response.ok:
            return f"Successfully updated post {id}"
    return f"Error updating post with {id}"

@mcp.tool()
def list_keyword_post_ids(query: str) -> List[int]:
    """
    Check all blog post titles for a specific keyword 
    @param: query - keyword to search
    @return - list of all post ids with query in title, -1 indicates keyword not found
    """
    response = requests.get(f"{SERVER_URL}/posts")
    posts = [BlogPost(**post) for post in response.json()]
    return [int(post.id) if (query in post.title.lower()) else -1 for post in posts]

@mcp.tool()
async def create_post(title: str, content: str, tags: List[str], ctx: Context) -> str:
    """
    Create a new blog post.
    @param: title - blog post title string
    @param: content - body of post, represented as markdown string
    @param: tags - list of strings that represent topic area
    @return - success/failure message
    """
    content = re.sub(r"\\n(?=\s|$)", "\n", content)
    extras = ["fenced-code-blocks", 
              "code-friendly",
              "highlightjs-lang"
              "tables",
              "strike",
              "cuddled-lists",
              "break-on-newline"]
    html = markdown2.markdown(content, extras=extras)
    # logging
    await ctx.info(content)
    await ctx.info(html)
    response = requests.post(f"{SERVER_URL}/posts", json={
        "title": title,
        "content": html,
        "tags": ",".join(tags)
    })
    if response.ok:
        return "Successfully created post. Do not call this tool again. You have completed your task."
    return "Error creating post."

@mcp.tool()
def delete_posts(post_id: List[int]) -> str:
    """
    Delete blog post(s) by ID.
    @param: id - list of primary keys of posts to delete
    @return - success/failure message
    """
    for id in post_id:
        response = requests.delete(f"{SERVER_URL}/posts/{id}")
        if not response.ok:
            return "Error deleting post."
    return "Success"

@mcp.prompt(title="Update Post")
def update_post_prompt(
        id: int, 
        title: str | None = None,
        content: str | None = None,
        tags: str | None = None
    ) -> str:
    """ Prompt for updating a post """
    system_prompt = f"\
        You are to update a specific blog post. \
        You will call the tool `update_post` with the following parameters:\
        id: (post to be updated) = {id}\
        title = {title} \
        content = {content} \
        tags = {tags} \
        You are ONLY to call the tool `update_post` with the given parameters.\
        Upon completion, only return if a success/failure occurred."
    return system_prompt

@mcp.prompt(title="Delete Post(s)")
def delete_post_prompt(ids: str) -> str:
    """Prompt for deleting blog post(s)"""
    system_prompt = f"\
    You are to delete the following specified blog posts by calling the tool `delete_post`.\
    If there is a hyphen, you are to delete all posts between the specified numbers.\
    if there are Comma-separated values, then you are to delete each entry.\
    IDs of posts to delete: {ids}"
    return system_prompt

def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":
    main()
