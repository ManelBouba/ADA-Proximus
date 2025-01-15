import random
import google.generativeai as genai
from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import urllib3
import json
import os

# Suppress HTTPS warnings for local testing (use only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure Gemini AI API
genai.configure(api_key="")  # Replace with your Gemini API key

# GoPhish API key
api = Gophish("", verify=False)

# Awareness Training Scenarios
training_examples = [
    {"Reason": "Password Security Awareness", "Educational Link": "https://example.com/security-tips"},
    {"Reason": "Recognizing Phishing Emails", "Educational Link": "https://example.com/phishing-tips"},
]

# SMTP Sending Profile Data
sending_profile_data = SMTP(
    name="Training Sending Profile",
    from_address="manelboubakeur1992@gmail.com",  # Replace with your email address
    from_name="Cybersecurity Trainer",
    reply_to_address="manelboubakeur1992@gmail.com",  # Replace with your email address
    host="smtp.gmail.com",  # Replace with your SMTP server host
    username="manelboubakeur1992@gmail.com",  # Replace with your SMTP username
    password="",  # Replace with your SMTP password
    port=587,  # SMTP port (use 465 for SSL, 587 for TLS)
    tls=True,  # Use TLS if needed
    ssl=False,  # Use SSL if needed
)

# Landing Page Data
landing_page_data = Page(
    name="Training Landing Page",
    url="https://localhost:3333/landing_pages",  # Replace with your actual training page URL
    html=""  # Can be updated with the actual HTML content if needed
)

# Generate a Training Email using Gemini AI
def generate_training_email():
    random_pick = random.choice(training_examples)
    prompt = f"""Write a professional email for cybersecurity training on the topic: {random_pick['Reason']}.\n
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
        print(f"SMTP Sending Profile created: {smtp.name}")
        return smtp.id  # Return the ID of the created SMTP object
    except Exception as e:
        print(f"Error creating SMTP profile: {e}")
        return None

# Create Landing Page
def create_landing_page():
    try:
        landing_page = api.pages.post(landing_page_data)
        print(f"Landing Page created: {landing_page.name}")
        return landing_page.id  # Return the ID of the created landing page
    except Exception as e:
        print(f"Error creating landing page: {e}")
        return None

# Create Email Template
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

        print(f"Email Template created: {template.name}")
        return template.id  # Return the ID of the created template
    except Exception as e:
        print(f"Error creating email template: {e}")
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

        print(f"Group created: {group.name}")
        return group.id  # Return the ID of the created group
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
        # Fetch the Template by ID
        template = api.templates.get(template_id)
        if not template:
            print(f"Error: Template with ID {template_id} not found.")
            return None
        
        # Fetch the SMTP Profile by ID
        smtp = api.smtp.get(sending_profile_id)
        if not smtp:
            print(f"Error: SMTP profile with ID {sending_profile_id} not found.")
            return None
        
        # Fetch the Landing Page by ID
        landing_page = api.pages.get(landing_page_id)
        if not landing_page:
            print(f"Error: Landing page with ID {landing_page_id} not found.")
            return None
        
        # Fetch the Group by ID
        group = api.groups.get(group_id)
        if not group:
            print(f"Error: Group with ID {group_id} not found.")
            return None

        # Create the campaign using the fetched objects
        campaign_data = Campaign(
            name="Cybersecurity Awareness Campaign",
            template=template,  # Use the fetched template object
            smtp=smtp,  # Use the fetched SMTP profile
            page=landing_page,  # Use the fetched landing page
            url="https://localhost:3333/landing_pages",
            groups=[group],  # Use the fetched group
        )

        # Post the campaign to GoPhish
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

    # Step 3: Create Landing Page and get phishing server link
    landing_page = create_landing_page()
    if not landing_page:
        print("Failed to create landing page. Exiting.")
        return
    phishing_server_link = landing_page.url  # Get phishing server link
    print(f"Phishing server link: {phishing_server_link}")  # Print the URL

    # Step 4: Create Email Template
    template_id = create_email_template(subject, body)
    if not template_id:
        print("Failed to create email template. Exiting.")
        return

    # Step 5: Create Group with Employees (Including positions)
    employees = [
        {"first_name": "John", "last_name": "Doe", "email": "wvaleaseabike@gmail.com", "position": "Manager"},
        {"first_name": "Jane", "last_name": "Smith", "email": "vandevelde.jan09@gmail.co", "position": "Developer"},
        {"first_name": "Mark", "last_name": "Taylor", "email": "manelbouman@gmail.com", "position": "Designer"}
    ]
    group_id = create_group(employees)
    if not group_id:
        print("Failed to create group. Exiting.")
        return

    # Step 6: Create Campaign
    campaign_id = create_campaign(template_id, sending_profile_id, landing_page.id, group_id)
    if campaign_id:
        print(f"Campaign successfully created with ID: {campaign_id}")
    else:
        print("Failed to create campaign.")

# Run the Main Workflow
if __name__ == "__main__":
    main()

