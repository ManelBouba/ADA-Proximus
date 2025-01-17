import random
import google.generativeai as genai
import urllib3
import json
import os
import logging

# Suppress HTTPS warnings for local testing (use only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        raise


config = load_config()

genai.configure(api_key=config["gemini_api_key"])

# Example training examples for generating emails
training_examples = [
    # {
    #     "Reason": "New Year opening party, hosted in Brussels offices, on 23th of January 2025, RSVP on  link",
    #     "Educational Link": "http://landing-page.com",
    #     "Created By": "Wim Vanhof",
    #     "id": "proximus",
    # },
    {
        "Reason": "Invitation to join the company's football league, for the next 2025-2026 season, already 80 precents, register now, deadline is next week, sent from Thomas Merlier, sales department for beautiful sports, connec to the platform to join an existing team or create your",
        "Educational Link": "http://landing-page.com",
        "Created By": "Thomas Merlier",
        "Company" : "Beautiful Sports",
        "id": "company_league"
    },
    {
        "Reason": "Register for our workshop, the topic of the training is Unconscious Bias Awareness",
        "Educational Link": "http://landing-page.com",
        "Created By": "Thomas Merlier",
        "Company" : "Proximus",
        "id": "Proximus"
    }
]


def generate_training_email():
    random_pick = random.choice(training_examples)
    prompt = f"""The sender’s name should be {random_pick['Created By']}.
The email should be about the theme: {random_pick["Reason"]}. 
This email will be sent automatically, so ensure there are no placeholders, text to be filled in, or anything requiring manual modification.
The email should be ready to send immediately, no things like that: -> [], or any other placeholders.
Nothing should be left for review or manual adjustment. link provided is {random_pick["Educational Link"]}.
    """
    # Generate Email Body
    try:
        email_body_response = genai.GenerativeModel("gemini-pro").generate_content(
            prompt
        )
        email_body = (
            email_body_response.text.strip() if email_body_response.text else None
        )
    except Exception as e:
        logging.error(f"Error generating email body: {e}")
        return None, None

    if not email_body:
        logging.error("Generated email body is empty.")
        return None, None

    # Generate Subject Line
    subject_prompt = f"Write an engaging subject line for the email body: {email_body}"
    try:
        email_subject_response = genai.GenerativeModel("gemini-pro").generate_content(
            subject_prompt
        )
        email_subject = (
            email_subject_response.text.strip() if email_subject_response.text else None
        )
    except Exception as e:
        logging.error(f"Error generating email subject: {e}")
        return None, None

    if not email_subject:
        logging.error("Generated email subject is empty.")
        return None, None

    logging.info(f"Generated Subject: {email_subject}")
    logging.info(f"Generated Body: {email_body}")
    return email_subject, email_body


email = generate_training_email()
