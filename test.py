import random
import google.generativeai as genai
from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import urllib3
import json
import os
import logging
import time

# Suppress HTTPS warnings for local testing (use only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from the config file
def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        raise

config = load_config()

# Configure Gemini AI API
genai.configure(api_key=config['gemini_api_key'])

# GoPhish API key
api = Gophish(config['gophish_api_key'], verify=False)
def load_html_with_placeholder(file_path, placeholder_dict):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            for placeholder, value in placeholder_dict.items():
                html_content = html_content.replace(f"{{{{{placeholder}}}}}", value)
            return html_content
    except Exception as e:
        logging.error(f"Error loading HTML file {file_path}: {e}")
        return None
# Awareness Training Scenarios
training_examples = [
    {"Reason": "Password Security Awareness", "Educational Link": "https://example.com/security-tips"},
    {"Reason": "Recognizing Phishing Emails", "Educational Link": "https://example.com/phishing-tips"},
]

# SMTP Sending Profile Data
sending_profile_data = SMTP(
    name="Training Sending Profile",
    from_address=config['smtp']['from_address'],
    from_name=config['smtp']['from_name'],
    reply_to_address=config['smtp']['reply_to_address'],
    host=config['smtp']['host'],
    username=config['smtp']['username'],
    password=config['smtp']['password'],
    port=config['smtp']['port'],
    tls=config['smtp']['tls'],
    ssl=config['smtp']['ssl'],
)

# Landing Page Data
landing_page_data = Page(
    name="Training Landing Page",
    #url=config['landing_page_url'],  # Load from config
    html=""  # Can be updated with the actual HTML content if needed
)

# Generate a more convincing Training Email using Gemini AI
def generate_training_email():
    random_pick = random.choice(training_examples)
    prompt = f"""Write a professional email for cybersecurity training on the topic: {random_pick['Reason']}.\n
    The email should be convincing and include this link for further reading: {random_pick['Educational Link']}.\n
    Use a friendly yet authoritative tone, and ensure that the reader feels compelled to take the course for their own security."""
    
    # Generate Email Body
    try:
        email_body_response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
        email_body = email_body_response.text.strip() if email_body_response.text else None
    except Exception as e:
        logging.error(f"Error generating email body: {e}")
        return None, None

    if not email_body:
        logging.error("Generated email body is empty.")
        return None, None

    # Generate Subject Line
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
        smtp = api.smtp.post(sending_profile_data)
        logging.info(f"SMTP Sending Profile created: {smtp.name}")
        return smtp.id  # Return the ID of the created SMTP object
    except Exception as e:
        logging.error(f"Error creating SMTP profile: {e}")
        return None

# Create Landing Page with full attributes
def create_landing_page():
    phishing_link = config["phishing_link"]
    landing_page_html = load_html_with_placeholder("landing_page.html", {"Tracker": phishing_link})

    if not landing_page_html:
        logging.error("Landing page HTML could not be loaded. Exiting.")
        return None

    try:
        landing_page_data = Page(
            name="Training Landing Page",
            html=landing_page_html,
            capture_credentials=True,  # Capture submitted credentials
            capture_passwords=True,  # Capture passwords as well
            redirect_url=phishing_link  # Redirect after submission
        )
        landing_page = api.pages.post(landing_page_data)
        logging.info(f"Landing Page created: {landing_page.name}")
        return landing_page
    except Exception as e:
        logging.error(f"Error creating landing page: {e}")
        return None

# Create Email Template
def create_email_template(subject, body, phishing_link):
    if not subject or not body:
        logging.error("Error: Subject or body is empty. Cannot create email template.")
        return None

    try:
        # Define the HTML and Text content for the email with more convincing language
        html_content = f"""<html><body><p>{body}</p><br><p><a href={{.URL}}>Click here</a> to learn more and protect your organization.</p></body></html>"""
        text_content = f"{body}\n\nClick here: {phishing_link}"

        # Create the template object
        template_data = Template(
            name="Cybersecurity Awareness Template",  # Template name
            subject=subject,  # The subject line of the email
            html=html_content,  # The HTML version of the email body
            text=text_content  # The plain-text version of the email body
        )

        # Post the template to GoPhish
        template = api.templates.post(template_data)

        logging.info(f"Email Template created: {template.name}")
        return template.id  # Return the ID of the created template
    except Exception as e:
        logging.error(f"Error creating email template: {e}")
        return None

# Create Group with Employees (with position)
def create_group(employees):
    try:
        # Create the user data list, including position
        user_data = [
            User(
                first_name=emp["first_name"], 
                last_name=emp["last_name"], 
                email=emp["email"],
                position=emp["position"]  # Add position
            ) for emp in employees
        ]

        # Create the group data
        group_data = Group(
            name="Employee Group",
            targets=user_data  # Add users to the group
        )

        # Post the group to GoPhish
        group = api.groups.post(group_data)

        logging.info(f"Group created: {group.name}")
        return group.id  # Return the ID of the created group
    except Exception as e:
        logging.error(f"Error creating group: {e}")
        return None
    
# Create Campaign with Open and Click Tracking
def create_campaign(template_id, sending_profile_id, landing_page_id, group_id):
    if not template_id or not sending_profile_id or not landing_page_id or not group_id:
        logging.error(f"Error: Missing required IDs for campaign creation. "
                      f"Template ID: {template_id}, Sending Profile ID: {sending_profile_id}, "
                      f"Landing Page ID: {landing_page_id}, Group ID: {group_id}")
        return None

    try:
        # Fetch the Template by ID
        template = api.templates.get(template_id)
        if not template:
            logging.error(f"Error: Template with ID {template_id} not found.")
            return None
        
        # Fetch the SMTP Profile by ID
        smtp = api.smtp.get(sending_profile_id)
        if not smtp:
            logging.error(f"Error: SMTP profile with ID {sending_profile_id} not found.")
            return None
        
        # Fetch the Landing Page by ID
        landing_page = api.pages.get(landing_page_id)
        if not landing_page:
            logging.error(f"Error: Landing page with ID {landing_page_id} not found.")
            return None
        
        # Fetch the Group by ID
        group = api.groups.get(group_id)
        if not group:
            logging.error(f"Error: Group with ID {group_id} not found.")
            return None

        # Create the campaign using the fetched objects with tracking enabled
        campaign_data = Campaign(
            name="Cybersecurity Awareness Campaign",
            template=template,  # Use the fetched template object
            smtp=smtp,  # Use the fetched SMTP profile
            page=landing_page,  # Use the fetched landing page
            url=config['phishing_link'],  # Use config URL for landing page
            groups=[group],  # Use the fetched group
            track_opens=True,  # Track email opens
            track_clicks=True,  # Track link clicks
        )

        # Post the campaign to GoPhish
        campaign = api.campaigns.post(campaign_data)
        logging.info(f"Campaign Created: {campaign.name}")
        logging.info(f"Campaign ID: {campaign.id}")
        return campaign.id  # Return the campaign ID

    except Exception as e:
        logging.error(f"Error creating campaign: {e}")
        return None

# Main Execution Workflow
def main():
    # Step 1: Generate training email content
    subject, body = generate_training_email()
    if not subject or not body:
        logging.error("Failed to generate training email content. Exiting.")
        return

    # Step 2: Create Sending Profile
    sending_profile_id = create_sending_profile()
    if not sending_profile_id:
        logging.error("Failed to create sending profile. Exiting.")
        return

    # Step 3: Create Landing Page and get phishing server link
    landing_page = create_landing_page()
    if not landing_page:
        logging.error("Failed to create landing page. Exiting.")
        return

    # Construct phishing server link using landing page ID
    phishing_server_link = f"{config['landing_page_url']}"
    logging.info(f"Phishing server link: {phishing_server_link}")
    
    # Step 4: Create Email Template with phishing link
    template_id = create_email_template(subject, body, phishing_server_link)
    if not template_id:
        logging.error("Failed to create email template. Exiting.")
        return

    # Step 5: Create Group with Employees (Including positions)
    employees = [
        {"first_name": "John", "last_name": "Doe", "email": "slhhamed@hotmail.com", "position": "Manager"},
        {"first_name": "Mark", "last_name": "Taylor", "email": "manelbouman@gmail.com", "position": "Designer"}
    ]
    group_id = create_group(employees)
    if not group_id:
        logging.error("Failed to create group. Exiting.")
        return

    # Step 6: Create Campaign
    campaign_id = create_campaign(template_id, sending_profile_id, landing_page.id, group_id)
    if campaign_id:
        logging.info(f"Campaign successfully created with ID: {campaign_id}")
    else:
        logging.error("Failed to create campaign.")

    # Optional: Add a delay to avoid hitting rate limits on the server
    time.sleep(2)  # Add sleep time between campaign creations to respect rate limits

# Run the Main Workflow
if __name__ == "__main__":
    main()
