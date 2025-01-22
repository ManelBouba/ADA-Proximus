import google.generativeai as genai  # type: ignore
import json
import os
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from email.mime.multipart import MIMEMultipart

import base64
import random
from email.mime.text import MIMEText
# Define the full path to the JSON file
CONFIG_FILE = "C:/Users/ilasv/gemini_email_sending_demo/config.json"
TOKEN_FILE = "C:/Users/ilasv/gemini_email_sending_demo/token.json"
CREDENTIALS_FILE = "C:/Users/ilasv/gemini_email_sending_demo/credentials.json"


phishing_examples = [
    # {"Reason": "Account Suspicious Activity", "Fake Link": "http://landing-page.com", "Created By": "IT Security Alerts"},
    # {"Reason": "Password Expiry Notification", "Fake Link": "http://landing-page.com", "Created By": "Password Management Service"},
    # {"Reason": "Exclusive Training Webinar On ", "Fake Link": "http://landing-page.com", "Created By": "Richard Rascal"},
    # {"Reason": "Email Storage Full", "Fake Link": "http://landing-page.com", "Created By": "Mail Admin"},
    # {"Reason": "Gmail Blocked Login", "Fake Link": "http://landing-page.com", "Created By": "Account Recovery Team"},
    {"Reason": "HR Policy Violation", "Fake Link": "https://alkszo.github.io/security-training/login_proximus.html", "Created By": "HR Department"},
    # {"Reason": "Microsoft Teams Missed Message", "Fake Link": "http://landing-page.com", "Created By": "Collaboration Support"},
    {"Reason": "DocuSign Signature Request by compagne", "Fake Link": "https://alkszo.github.io/security-training/login_proximus.html", "Created By": "Document Sign Service"},
    # {"Reason": "Job Opportunity intern!!!", "Fake Link": "http://landing-page.com", "Created By": "Recruitment Team"}
    # {"Reason": "Fake Meeting", "Fake Link": "http://landing-page.com", "Created By": "Meeting Coordinator"}
]



# Load configuration
# Define the list of recipients
recipients = [
    {"email": "wout.vanaert.visma@proton.me", "name": "Wout Van Aert", "position": "Contact Center Agent"},
    # {"email": "remco.evenepoel.soudal@proton.me", "name": "Remco Evenepoel", "position": "Customer Service Specialist"},
    # {"email": "tadej.pogacar.uae@proton.me", "name": "Tadej Pogacar", "position": "Sales Advisor"},
    # {"email": "arnaud.de.lie.lotto@proton.me", "name": "Arnaud De Lie", "position": "B2B Sales Representative"},
    # {"email": "mathieu.vanderpoel.alpecin@proton.me", "name": "Mathieu Van Der Poel", "position": "Senior Legal Advisor"},
    # {"email": "julian.alaphilippe.tudor@proton.me", "name": "Julian Alaphilippe", "position": "Payroll Officer"},
    # {"email": "tom.pidcock.q365@proton.me", "name": "Tom Pidcock", "position": "Compensation & Benefits Specialist"},
    # {"email": "ben.oconnor.decathlon@proton.me", "name": "Ben O'Connor", "position": "Finance Business Partner"},
    # {"email": "jonas.vinegegaard.visma@proton.me", "name": "Jonas Vingegaard", "position": "Finance Specialist"},
    # {"email": "victor.campenaerts@proton.me", "name": "Victor Campenaerts", "position": "Technical Dispatching"}
]

# Load configuration
def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

# Initialize generative AI model
def initialize_genai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# Generate email content
def generate_email_content(model, name, surname, position):
    # Take a random reason from phishing examples
    global random_pick 
    random_pick = random.choice(phishing_examples)

    # Formulate the prompt, avoiding placeholders like [topic] and [date]
    # 
    prompt = f""""Compose a professional email from {random_pick["Created By"]} to {name} {surname}, who is a {position}, addressing the topic: {random_pick["Reason"]}.

Structure the email as follows:

Opening: A friendly yet professional greeting.
Introduction: Briefly introduce the topic and why it is relevant to {name} {surname}.
Explanation: Clearly and concisely explain the significance of {random_pick["Reason"]} in 2–3 sentences.
Closing: End with a polite and actionable request that encourages {name} {surname} to respond or take the next step.
Tone and Style:

Professional, persuasive, and warm, with an optional hint of urgency (without being alarming).
Use natural and realistic language tailored to the recipient's role as a {position}.
Avoid overused words such as "crucial," "vital," "rare," or "urgent."
Requirements:

Use 75–100 words in total.
Avoid placeholders (e.g., '[Date and Time]') and special formatting (e.g., brackets '[]', '()', or '* **')..
Avoid references to links or phrases like "click here."
Write only the body of the email, and ensure it is free of grammatical errors.
Use varied sentence structures and vocabulary to create a polished, engaging, and professional email.
 Do not include the subject in the body email.
Signed, {random_pick["Created By"]}.
"""
#f"""Compose a professional and well-crafted email from {random_pick["Created By"]} to {name} {surname}, who is a {position}. The email should address the following topic: {random_pick["Reason"]}.

# The email must include:

# A clear explanation of why {random_pick['Reason']} is important, expressed in natural and realistic language.
# A tone that is professional, persuasive, and just a little bet urgent (but not overly alarming to avoid suspicion).
# A personalized touch tailored to the recipient: {name} {surname}.

# Flawless grammar and smooth phrasing, avoiding awkward or unnatural expressions.
# A word count of 75–100 words.
# A subject line free of special characters (e.g., brackets or symbols).
# Additional Conditions:

# Avoid placeholders (e.g., '[Date and Time]') and special formatting (e.g., brackets '[]', '()', or '* **').
# Do not include any reference to clicking links or similar actions.
# Do not use words like "crucial," "vital," "rare," or "urgent."
# Write only the body of the email, ensuring it is ready to send.
# Do not include the subject in the body email.
# Signed, {random_pick["Created By"]}
# """




    # Generate the body of the email using the correct method
    body = model.generate_content(prompt)

    # Generate the subject of the email
    subject = model.generate_content(f"Write me the subject of this email:\n{body.text}")
    print(subject.text)
    print(body.text)
    
    return subject.text, body.text  

# Create a message for an email
def create_message(sender, to, subject, message_html):
    message = MIMEMultipart('alternative')
    message.attach(MIMEText(message_html, 'html'))
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


# Send an email message
def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! Message ID: {sent_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

# Authenticate and get Gmail service
def get_gmail_service(scopes, token_file, credentials_file):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def main():
    config = load_config(CONFIG_FILE)
    GEMINI_API_KEY = config.get("GEMINI_API_KEY")
    model = initialize_genai(GEMINI_API_KEY)
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    service = get_gmail_service(SCOPES, TOKEN_FILE, CREDENTIALS_FILE)

    for recipient in recipients:
        name = recipient["name"].split()[0]
        surname = " ".join(recipient["name"].split()[1:])
        email = recipient["email"]
        position = recipient["position"]

        subject, body = generate_email_content(model, name, surname, position)
        body = body.replace("\n", "<br>").replace("\n\n", "<p></p>")
        print(body)
        css_styles = """
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        .email-container {
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .email-header {
            text-align: center;
            padding: 20px;
            background-color: #f4f4f4;
            border-bottom: 1px solid #dddddd;
        }
        .email-header img {
            max-width: 150px;
            height: auto;
        }
        .email-body {
            padding: 20px;
            color: #333333;
            line-height: 1.6;
            text-align: left;
        }
        .button-container {
            text-align: center;
            margin: 20px 0;
        }
        .button {
            background-color: #5C2D91;
            color: #ffffff;
            padding: 12px 24px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            display: inline-block;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #4b2377;
        }
        .footer {
            text-align: center;
            padding: 10px;
            font-size: 12px;
            color: #888888;
            background-color: #f4f4f4;
            border-top: 1px solid #dddddd;
        }
    </style>
"""

        message = create_message("me", email, subject,
                              f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .email-container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .rs-border-c2 {{
            border: 3px solid #5C2D91;
            padding: 20px;
        }}
        .email-header {{
            text-align: center;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .email-header img {{
            max-width: 150px;
            height: auto;
        }}
        .email-body {{
            padding: 20px;
            color: #333333;
            text-align: left;
        }}
        .button-container {{
            text-align: center;
            margin-top: 20px;
        }}
        .button {{
            background-color: #5C2D91;
            color: #ffffff;
            padding: 12px 24px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            display: inline-block;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
        <img alt="Company Logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Proximus_logo_2014.svg/1280px-Proximus_logo_2014.svg.png" />
        </div>
        <div class="email-body">
            {body}
            <p>{{.Tracker}}</p>
        </div>
        <div class="button-container">
            <a href="{random_pick["Fake Link"]}" class="button">Click Here</a>
        </div>
    </div>
</body>
</html>
""")
                                 
        send_message(service, "me", message)

if __name__ == "__main__":
    main()
