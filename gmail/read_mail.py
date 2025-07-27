# read_mail.py
from googleapiclient.discovery import build
from .oauth import get_gmail_credentials

def list_messages(service, max_results=10):
    response = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()
    return response.get("messages", [])

def get_message(service, msg_id):
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    snippet = msg.get("snippet")
    return headers, snippet

def read_latest_emails(max_results=5):
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)

    msgs = list_messages(service, max_results=max_results)
    if not msgs:
        print("No messages found.")
        return

    data = ""
    for m in msgs:
        hdrs, snippet = get_message(service, m["id"])
        subject = hdrs.get("Subject", "(no subject)")
        sender  = hdrs.get("From", "(unknown)")
        data += f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n---\n"
    return data

def main():
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)

    msgs = list_messages(service, max_results=5)
    for m in msgs:
        hdrs, snippet = get_message(service, m["id"])
        subject = hdrs.get("Subject", "(no subject)")
        sender  = hdrs.get("From", "(unknown)")
        print(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n---")

if __name__ == "__main__":
    main()
