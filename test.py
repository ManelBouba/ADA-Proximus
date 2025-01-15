import random
import google.generativeai as genai
from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import urllib3
import json
import os

# Suppress HTTPS warnings for local testing (use only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load configuration file
config_file = "config.json"  # Replace with your JSON file's name if different
if os.path.exists(config_file):
    with open(config_file, "r") as file:
        config = json.load(file)
        GEMINI_API_KEY = config.get("GEMINI_API_KEY")  # Fetch Gemini API key from config
        GOPHISH_API_KEY = config.get("GOPHISH_API_KEY")  # Fetch Gophish API key from config
else:
    raise FileNotFoundError(f"Configuration file '{config_file}' not found.")

# Validate API keys
if not GEMINI_API_KEY or not GOPHISH_API_KEY:
    raise ValueError("Both GEMINI_API_KEY and GOPHISH_API_KEY must be defined in the config.")

# Configure Gemini AI API
genai.configure(api_key=GEMINI_API_KEY)

# GoPhish API initialization
api = Gophish(GOPHISH_API_KEY, verify=False)

# Awareness Training Scenarios
training_examples = [
    {"Reason": "Password Security Awareness", "Educational Link": "https://example.com/security-tips"},
    {"Reason": "Recognizing Phishing Emails", "Educational Link": "https://example.com/phishing-tips"},
]

# SMTP Sending Profile Data
sending_profile_data = SMTP(
    name="Training Sending Profile",
    from_address="-",  # Replace with your email address
    from_name="Cybersecurity Trainer",
    reply_to_address="",  # Replace with your email address
    host="smtp.example.com",  # Replace with your SMTP server host
    username="smtp_user",  # Replace with your SMTP username
    password="",  # Replace with your SMTP password
    port=587,  # SMTP port (use 465 for SSL, 587 for TLS)
    tls=True,  # Use TLS if needed
    ssl=False,  # Use SSL if needed
)

# Landing Page Data
landing_page_data = Page(
    name="Training Landing Page",
    url="https://www.cybersecuritytraining.com",  # Replace with your actual training page URL
    html=""  # Can be updated with the actual HTML content if needed
)

# Generate a Training Email using Gemini AI
def generate_training_email():
    random_pick = random.choice(training_examples)
    prompt = f"""Write a professional email for cybersecurity training on the topic: {random_pick['Reason']}.
    Include this link for further reading: {random_pick['Educational Link']}."""

    # Generate Email Body
    email_body_response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    email_body = email_body_response.text.strip() if email_body_response.text else None

    if not email_body:
        print("Error: Generated email body is empty.")
        return None, None

    # Generate Subject Line
    subject_prompt = f"Write an engaging subject line for the email body: {email_body}"
    email_subject_response = genai.GenerativeModel("gemini-pro").generate_content(subject_prompt)
    email_subject = email_subject_response.text.strip() if email_subject_response.text else None

    if not email_subject:
        print("Error: Generated email subject is empty.")
        return None, None

    print(f"Generated Subject: {email_subject}")
    print(f"Generated Body: {email_body}")
    return email_subject, email_body

# Create Sending Profile
def create_sending_profile():
    try:
        smtp = api.smtp.post(sending_profile_data)
        print(f"Sending Profile Created: {smtp.name}")
        return smtp.id  # Return the SMTP profile ID
    except Exception as e:
        print(f"Error creating sending profile: {e}")
        return None

# Create Landing Page
def create_landing_page():
    try:
        landing_page = api.pages.post(landing_page_data)
        print(f"Landing Page Created: {landing_page.name}")
        return landing_page.id  # Return the landing page ID
    except Exception as e:
        print(f"Error creating landing page: {e}")
        return None

# Function to create a new template
def create_email_template(subject, body):
    if not subject or not body:
        print("Error: Subject or body is empty. Cannot create email template.")
        return None

    try:
        # Define the HTML and Text content for the email
        html_content = f"""<html><body><p>{body}</p><br><p><a href="{{.URL}}">Click here</a> for more information.</p></body></html>"""
        text_content = f"{body}\n\nClick here: {{.URL}}"

        # Create the template object
        template_data = Template(
            name="Cybersecurity Awareness Template",  # Template name
            subject=subject,  # The subject line of the email
            html=html_content,  # The HTML version of the email body
            text=text_content  # The plain-text version of the email body
        )

        # Post the template to GoPhish
        template = api.templates.post(template_data)

        print(f"Template Created: {template.name}")
        print(f"Template ID: {template.id}")
        return template.id  # Return the template ID
    except Exception as e:
        print(f"Error creating template: {e}")
        return None

# Create Group with Users
def create_group():
    try:
        user_data = [
            User(
                first_name="John",
                last_name="Doe",
                email="" #replace by user email
            )
        ]
        
        group_data = Group(
            name="Cybersecurity Training Group",
            targets=user_data  # Add the user to the group
        )
        
        group = api.groups.post(group_data)
        print(f"Group Created: {group.name} with ID: {group.id}")
        return group.id  # Return the group ID
    except Exception as e:
        print(f"Error creating group: {e}")
        return None

# Create Campaign
def create_campaign(template_id, sending_profile_id, landing_page_id, group_id):
    if not template_id or not sending_profile_id or not landing_page_id or not group_id:
        print(f"Error: Missing required IDs for campaign creation. "
              f"Template ID: {template_id}, Sending Profile ID: {sending_profile_id}, "
              f"Landing Page ID: {landing_page_id}, Group ID: {group_id}")
        return None

    try:
        # Print debugging information to verify the IDs
        print(f"Creating Campaign with the following parameters:")
        print(f"Template ID: {template_id}")
        print(f"Sending Profile ID: {sending_profile_id}")
        print(f"Landing Page ID: {landing_page_id}")
        print(f"Group ID: {group_id}")
        
        # Ensure Template ID is correctly assigned
        template = Template(id=template_id)
        
        # Create campaign data using the correct Template object
        campaign_data = Campaign(
            name="Cybersecurity Awareness Campaign",
            template=template,  # Correct reference to Template object
            smtp=SMTP(id=sending_profile_id),
            page=Page(id=landing_page_id),
            url="https://www.cybersecuritytraining.com",  # URL for training
            groups=[Group(id=group_id)],  # Group IDs to target
        )
        
        # Post the campaign data to GoPhish
        campaign = api.campaigns.post(campaign_data)
        print(f"Campaign Created: {campaign.name}")
        print(f"Campaign ID: {campaign.id}")
        return campaign.id  # Return the campaign ID
    except Exception as e:
        print(f"Error creating campaign: {e}")
        return None

# Main Execution Workflow
def main():
    # Step 1: Generate training email content
    subject, body = generate_training_email()
    if not subject or not body:
        print("Failed to generate training email content. Exiting.")
        return

    # Step 2: Create Sending Profile
    sending_profile_id = create_sending_profile()
    if not sending_profile_id:
        print("Failed to create sending profile. Exiting.")
        return

    # Step 3: Create Landing Page
    landing_page_id = create_landing_page()
    if not landing_page_id:
        print("Failed to create landing page. Exiting.")
        return

    # Step 4: Create Email Template
    template_id = create_email_template(subject, body)
    if not template_id:
        print("Failed to create email template. Exiting.")
        return

    # Step 5: Create Group
    group_id = create_group()
    if not group_id:
        print("Failed to create group. Exiting.")
        return

    # Step 6: Create Campaign
    campaign_id = create_campaign(template_id, sending_profile_id, landing_page_id, group_id)
    if campaign_id:
        print(f"Campaign successfully created with ID: {campaign_id}")
    else:
        print("Failed to create campaign.")

# Run the Main Workflow
if __name__ == "__main__":
    main()
