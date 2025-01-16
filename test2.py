import random
import json
import logging
import os
import urllib3
from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import google.generativeai as genai

# Suppress HTTPS warnings for local testing (use only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Load configuration from the config file
def load_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        raise


config = load_config()

# Configure Gemini AI API
genai.configure(api_key=config["gemini_api_key"])

# GoPhish API key
api = Gophish(config["gophish_api_key"], verify=False)


# Load HTML and replace placeholders
def load_html_with_placeholder(file_path, placeholder_dict):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            for placeholder, value in placeholder_dict.items():
                html_content = html_content.replace(f"{{{placeholder}}}", value)
            return html_content
    except Exception as e:
        logging.error(f"Error loading HTML file {file_path}: {e}")
        return None


# Awareness Training Scenarios
training_examples = [
    {"Reason": "Password Security Awareness", "Educational Link": "https://example.com/security-tips"},
    {"Reason": "Recognizing Phishing Emails", "Educational Link": "https://example.com/phishing-tips"},
]


# Generate a more convincing Training Email using Gemini AI
def generate_training_email():
    random_pick = random.choice(training_examples)
    prompt = f"""Write a professional email for cybersecurity training on the topic: {random_pick['Reason']}.\n
    The email should be convincing and include this link for further reading: {random_pick['Educational Link']}.\n
    Use a friendly yet authoritative tone, and ensure that the reader feels compelled to take the course for their own security."""
    try:
        # Generate email body
        email_body_response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        email_body = email_body_response.text.strip() if email_body_response.text else None
    except Exception as e:
        logging.error(f"Error generating email body: {e}")
        return None, None

    if not email_body:
        logging.error("Generated email body is empty.")
        return None, None

    # Generate subject line
    subject_prompt = f"Write an engaging subject line for the email body: {email_body}"
    try:
        email_subject_response = genai.GenerativeModel("gemini-pro").generate_content(subject_prompt)
        email_subject = email_subject_response.text.strip() if email_subject_response.text else None
    except Exception as e:
        logging.error(f"Error generating email subject: {e}")
        return None, None

    if not email_subject:
        logging.error("Generated email subject is empty.")
        return None, None

    logging.info(f"Generated Subject: {email_subject}")
    logging.info(f"Generated Body: {email_body}")
    return email_subject, email_body


# Create Sending Profile
def create_sending_profile():
    try:
        smtp_data = SMTP(
            name="Training Sending Profile",
            from_address=config["smtp"]["from_address"],
            from_name=config["smtp"]["from_name"],
            reply_to_address=config["smtp"]["reply_to_address"],
            host=config["smtp"]["host"],
            username=config["smtp"]["username"],
            password=config["smtp"]["password"],
            port=config["smtp"]["port"],
            tls=config["smtp"]["tls"],
            ssl=config["smtp"]["ssl"],
        )
        smtp = api.smtp.post(smtp_data)
        logging.info(f"SMTP Sending Profile created: {smtp.name}")
        return smtp.id
    except Exception as e:
        logging.error(f"Error creating SMTP profile: {e}")
        return None


# Create Landing Page
def create_landing_page():
    phishing_link = config["phishing_link"]
    landing_page_html = load_html_with_placeholder("landing_page.html", {"Tracker": phishing_link})

    if not landing_page_html:
        logging.error("Landing page HTML could not be loaded. Exiting.")
        return None

    try:
        landing_page_data = Page(
            name="Training Landing Page",
            url=config["landing_page_url"],
            html=landing_page_html,
        )
        landing_page = api.pages.post(landing_page_data)
        logging.info(f"Landing Page created: {landing_page.name}")
        return landing_page
    except Exception as e:
        logging.error(f"Error creating landing page: {e}")
        return None


# Create Email Template
def create_email_template(subject, body):
    phishing_link = config["phishing_link"]
    email_template_html = load_html_with_placeholder(
        "email_template.html", {"body": body, "phishing_link": phishing_link}
    )

    if not email_template_html:
        logging.error("Email template HTML could not be loaded. Exiting.")
        return None

    try:
        template_data = Template(
            name="Cybersecurity Awareness Template",
            subject=subject,
            html=email_template_html,
            text=f"{body}\n\nClick here: {phishing_link}",
        )
        template = api.templates.post(template_data)
        logging.info(f"Email Template created: {template.name}")
        return template.id
    except Exception as e:
        logging.error(f"Error creating email template: {e}")
        return None


# Create Group
def create_group(employees):
    try:
        user_data = [
            User(first_name=emp["first_name"], last_name=emp["last_name"], email=emp["email"], position=emp["position"])
            for emp in employees
        ]
        group_data = Group(name="Employee Group", targets=user_data)
        group = api.groups.post(group_data)
        logging.info(f"Group created: {group.name}")
        return group.id
    except Exception as e:
        logging.error(f"Error creating group: {e}")
        return None


# Create Campaign
def create_campaign(template_id, sending_profile_id, landing_page_id, group_id):
    if not all([template_id, sending_profile_id, landing_page_id, group_id]):
        logging.error("Error: Missing required IDs for campaign creation.")
        return None

    try:
        campaign_data = Campaign(
            name="Cybersecurity Awareness Campaign",
            template=api.templates.get(template_id),
            smtp=api.smtp.get(sending_profile_id),
            page=api.pages.get(landing_page_id),
            groups=[api.groups.get(group_id)],
            url=config["landing_page_url"],
            track_opens=True,
            track_clicks=True,
        )
        campaign = api.campaigns.post(campaign_data)
        logging.info(f"Campaign Created: {campaign.name}")
        logging.info(f"Campaign ID: {campaign.id}")
        return campaign.id
    except Exception as e:
        logging.error(f"Error creating campaign: {e}")
        return None


# Main Workflow
def main():
    subject, body = generate_training_email()
    if not subject or not body:
        logging.error("Failed to generate training email content. Exiting.")
        return

    sending_profile_id = create_sending_profile()
    if not sending_profile_id:
        return

    landing_page = create_landing_page()
    if not landing_page:
        return

    template_id = create_email_template(subject, body)
    if not template_id:
        return

    employees = [
        {"first_name": "John", "last_name": "Doe", "email": "wvaleaseabike@gmail.com", "position": "Manager"},
        {"first_name": "Jane", "last_name": "Smith", "email": "vandevelde.jan09@gmail.com", "position": "Developer"},
        {"first_name": "Mark", "last_name": "Taylor", "email": "manelbouman@gmail.com", "position": "Designer"}
    ]
    group_id = create_group(employees)
    if not group_id:
        return

    campaign_id = create_campaign(template_id, sending_profile_id, landing_page.id, group_id)
    if campaign_id:
        logging.info(f"Campaign successfully created with ID: {campaign_id}")
    else:
        logging.error("Failed to create campaign.")


if __name__ == "__main__":
    main()
