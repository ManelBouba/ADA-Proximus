import random
import google.generativeai as genai
from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import urllib3
import json
import os
import logging

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

# Awareness Training Scenarios
training_examples = [
    {"Reason": "Account Suspicious Activity", "Educational Link": "http://landing-page.com", "Created By": "Sam Sussy", "id" : " 1"},
    {"Reason": "Password Expiry Notification", "Educational Link": "http://landing-page.com", "Created By": "Sally Sneaky", "id" : "2"},
    {"Reason": "Exclusive Training Webinar", "Educational Link": "http://landing-page.com", "Created By": "Richard Rascal", "id" : "3"},
    {"Reason": "Email Storage Full", "Educational Link": "http://landing-page.com", "Created By": "Bernard Bandit", "id" : "4"},
    {"Reason": "Team Gathering Invitation", "Educational Link": "http://landing-page.com", "Created By": "Paul Ploy", "id" : "6"},
    {"Reason": "Upcoming Meeting Notice", "Educational Link": "http://landing-page.com", "Created By": "Olivia Opportunist", "id" : "7"},
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
    url=config['landing_page_url'],  # Load from config
    html=""  # Can be updated with the actual HTML content if needed
)

# Generate a more convincing Training Email using Gemini AI
def generate_training_email():
    random_pick = random.choice(training_examples)
    prompt = f"""Write an email following those constraints:
    The sender who signs is {random_pick['Created By']}
    The email should be about the theme: {random_pick["Reason"]}.
    The email should:
    * Sound professional, persuasive, and engaging
    * Be free of placeholders like '[Date and Time]' or '[Target Audience]' or ['Date'], if talking about time, use 'next week'.
    * Be completely free of any placeholders or brackets (e.g., '[]','()').
    * Appear ready to be sent immediately.
    Provide the email content directly. Do not include any additional instructions or formatting"""
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

# Create Landing Page
def create_landing_page():
    try:
        landing_page = api.pages.post(landing_page_data)
        logging.info(f"Landing Page created: {landing_page.name}")
        return landing_page  # Return the full landing page object, not just the ID
        print(landing_page)
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
        html_content = f"""<html><body><p>{body}</p><br><p><a href="{phishing_link}">Click here</a> to learn more and protect your organization.</p></body></html>"""
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
            url=config['landing_page_url'],  # Use config URL for landing page
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
    phishing_server_link = f"{config['go_phish_server_url']}/p/{landing_page.id}"
    logging.info(f"Phishing server link: {phishing_server_link}")
    
    # Step 4: Create Email Template with phishing link
    template_id = create_email_template(subject, body, phishing_server_link)
    if not template_id:
        logging.error("Failed to create email template. Exiting.")
        return

    # Step 5: Create Group with Employees (Including positions)
    employees = [
    {"first_name": "John", "last_name": "Doe", "email": "wvaleaseabike@gmail.com", "position": "Manager"},
    {"first_name": "Jane", "last_name": "Smith", "email": "vandevelde.jan09@gmail.co", "position": "Developer"},
    {"first_name": "Mark", "last_name": "Taylor", "email": "manelbouman@gmail.com", "position": "Designer"},
    {"first_name": "Wout", "last_name": "Van Aert", "email": "wout.vanaert.visma@proton.me", "position": "Contact Center Agent"},
    {"first_name": "Remco", "last_name": "Evenepoel", "email": "remco.evenepoel.soudal@proton.me", "position": "Customer Service Specialist"},
    {"first_name": "Tadej", "last_name": "Pogacar", "email": "tadej.pogacar.uae@proton.me", "position": "Sales Advisor"},
    {"first_name": "Arnaud", "last_name": "De Lie", "email": "arnaud.de.lie.lotto@proton.me", "position": "B2B Sales Representative"},
    {"first_name": "Mathieu", "last_name": "Van Der Poel", "email": "mathieu.vanderpoel.alpecin@proton.me", "position": "Senior Legal Advisor"},
    {"first_name": "Julian", "last_name": "Alaphilippe", "email": "julian.alaphilippe.tudor@proton.me", "position": "Payroll Officer"},
    {"first_name": "Tom", "last_name": "Pidcock", "email": "tom.pidcock.q365@proton.me", "position": "Compensation & Benefits Specialist"},
    {"first_name": "Ben", "last_name": "O'Connor", "email": "ben.oconnor.decathlon@proton.me", "position": "Finance Business Partner"},
    {"first_name": "Jonas", "last_name": "Vingegaard", "email": "jonas.vinegegaard.visma@proton.me", "position": "Finance Specialist"},
    {"first_name": "Victor", "last_name": "Campenaerts", "email": "victor.campenaerts@proton.me", "position": "Technical Dispatching"}
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

# Run the Main Workflow
if __name__ == "__main__":
    main()
