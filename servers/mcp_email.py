"""
MCP server for managing email interactions.
- Read Emails, Send Emails, Summarize Emails
"""
from mcp.server.fastmcp import FastMCP
from gmail import read_mail, send_mail

mcp = FastMCP("Email Server", version="0.1.0")


@mcp.tool(title="Read Emails", description="List the latest emails in your inbox.")
def read_emails() -> str:
    """Read the latest 5 emails."""
    return read_mail.read_latest_emails()

@mcp.tool(title="Send Email", description="Send an email to a specified recipient.")
def send_email(to: str, subject: str, body: str) -> str:
    sent = send_mail.send_email(to, subject, body)
    if sent:
        return f"Email sent successfully to {to} with subject '{subject}'."
    else:
        return "Failed to send email."

def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":
    main()