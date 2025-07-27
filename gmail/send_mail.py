# send_mail.py
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from .oauth import get_gmail_credentials

def create_message(to, subject, body_text):
    message = MIMEText(body_text)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def send_message(service, message):
    sent = service.users().messages().send(
        userId="me", body=message
    ).execute()
    print("Message Id:", sent["id"])
    return sent

def send_email(to, subject, body_text):
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)
    message = create_message(to, subject, body_text)
    return send_message(service, message)

def main():
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)

    msg = create_message(
        to="friend@example.com",
        subject="Hello from Python!",
        body_text="This is a test email sent via the Gmail API."
    )
    send_message(service, msg)

if __name__ == "__main__":
    main()
