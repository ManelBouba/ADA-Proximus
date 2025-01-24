from user_loader import load_users_from_csv
from email_generator import generate_email_content
from gophish_api import GophishAPI
import json

def main():
    # Load configuration
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Initialize Gophish API
    gophish_api = GophishAPI(config["gophish_api_key"], config["gophish_url"])

    # Load users
    users = load_users_from_csv(config["user_group_csv"])

    # Generate emails for each user
    for user in users:
        email_subject, email_body = generate_email_content(
            config["GEMINI_API_KEY"],
            user.first_name,
            user.last_name,
            user.position
        )

        # Create and upload email template
        email_template_id = gophish_api.create_email_template(
            subject=email_subject,
            html_content=email_body
        )

        # Create and upload user group
        user_group_id = gophish_api.create_user_group(users)

        # Create and upload landing page
        landing_page_id = gophish_api.create_landing_page("landing_page.html")

        # Create phishing campaign
        gophish_api.create_campaign(
            campaign_name="Phishing Test Campaign",
            template_id=email_template_id,
            page_id=landing_page_id,
            smtp_profile_id=config["smtp_profile_id"],
            user_group_id=user_group_id
        )

if __name__ == "__main__":
    main()
