import random
import json
import logging
from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
from requests.exceptions import RequestException
import urllib3

# Suppress HTTPS warnings for local testing (use only for local dev)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from a JSON file
def load_config(config_file="config.json"):
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
            return config.get("gophish_api_key"), config.get("gmail_pass")
    except FileNotFoundError as e:
        logger.error(f"Config file not found: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    return None, None

# Initialize Gophish API
def initialize_gophish(api_key):
    try:
        return Gophish(api_key, verify=False)
    except RequestException as e:
        logger.error(f"Error initializing Gophish API: {e}")
    return None

# Create SMTP sending profile
def create_smtp_profile(phish_api, gmail_pass):
    try:
        sending_profile = SMTP(
            name="Document Sign",
            from_address="manelboubakeur1992@gmail.com",  
            from_name="Docusign",
            reply_to_address="manelboubakeur1992@gmail.com",  
            host="smtp.gmail.com:587",  
            username="manelboubakeur1992@gmail.com",  
            password=gmail_pass,  
            port=587,  
            tls=True,  
            ssl=False  
        )
        return phish_api.smtp.post(sending_profile)
    except RequestException as e:
        logger.error(f"Error creating SMTP profile: {e}")
    return None

# Create a landing page
def create_landing_page(phish_api, html_content):
    try:
        landing_page = Page(
            name="Document Sign Page",
            url="127.0.0.1:3333",
            html=html_content,
            capture_credentials=True,
            capture_passwords=True
        )
        return phish_api.pages.post(landing_page)
    except RequestException as e:
        logger.error(f"Error creating landing page: {e}")
    return None

# Create email template
def create_email_template(phish_api, html_content):
    try:
        email_template = Template(
            name="Docu Sign Scam",
            subject="Sign Company Documents",
            html=html_content
        )
        return phish_api.templates.post(email_template)
    except RequestException as e:
        logger.error(f"Error creating email template: {e}")
    return None

# Create user group
def create_user_group(phish_api):
    try:
        group = Group(
            name="Example Gr",
            targets=[User(first_name='Alek', last_name='Szostakowski', email='manelbouman@gmail.com', position='data janitor')]
        )
        return phish_api.groups.post(group)
    except RequestException as e:
        logger.error(f"Error creating user group: {e}")
    return None

# Create phishing campaign
def create_phishing_campaign(phish_api, template, page, smtp, group):
    try:
        campaign = Campaign(
            name="Document Sign Scam",
            template=template,
            page=page,
            smtp=smtp,
            groups=[group],
            url="http://127.0.0.1"
        )
        return phish_api.campaigns.post(campaign)
    except RequestException as e:
        logger.error(f"Error creating phishing campaign: {e}")
    return None

# Display campaign results
def display_campaign_results(phish_api, campaign_id):
    try:
        campaign = phish_api.campaigns.get(campaign_id)
        for result in campaign.results:
            logger.info(f"Result: {result.__dict__}")
    except RequestException as e:
        logger.error(f"Error fetching campaign results: {e}")

# Main function to execute all steps
def main():
    # Step 1: Load configuration
    api_key, gmail_pass = load_config()
    if not api_key or not gmail_pass:
        logger.error("API key or Gmail password not found in config.")
        return

    # Step 2: Initialize Gophish API
    phish_api = initialize_gophish(api_key)
    if not phish_api:
        return

    # Step 3: Create SMTP profile
    smtp = create_smtp_profile(phish_api, gmail_pass)
    if not smtp:
        return

    # Step 4: Load HTML for landing page
    try:
        with open("landing_page.html", "r") as file:
            landing_html = file.read()
    except FileNotFoundError as e:
        logger.error(f"Landing page HTML not found: {e}")
        return

    # Step 5: Create landing page
    page = create_landing_page(phish_api, landing_html)
    if not page:
        return

    # Step 6: Load email template HTML
    try:
        with open('email_template.html') as file:
            email_html = file.read()
    except FileNotFoundError as e:
        logger.error(f"Email template HTML not found: {e}")
        return

    # Step 7: Create email template
    template = create_email_template(phish_api, email_html)
    if not template:
        return

    # Step 8: Create user group
    group = create_user_group(phish_api)
    if not group:
        return

    # Step 9: Create phishing campaign
    campaign = create_phishing_campaign(phish_api, template, page, smtp, group)
    if not campaign:
        return

    # Step 10: Display campaign results
    display_campaign_results(phish_api, campaign.id)

if __name__ == "__main__":
    main()
