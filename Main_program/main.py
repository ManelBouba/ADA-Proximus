import Gophish_runner, landing_page, email_generator, file_reader
import json
import urllib3
urllib3.disable_warnings()


with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    """
    Main function to run the Gophish campaign automation.
    This function performs the following steps:
    1. Reads target data from a CSV file.
    2. Initializes a Gophish instance with the provided configuration.
    3. Clears existing sending profiles, landing pages, email templates, groups, and campaigns in Gophish.
    4. Creates a new sending profile and landing page.
    5. For each target (limited to the first target in this example):
        - Generates email content using the email generator.
        - Creates an email template in Gophish.
        - Creates a group in Gophish.
        - Creates a campaign in Gophish.
    6. If the config file indicates scheduling, the programm will run campaigns for each recipient and then 
    schedule following ones according to configuration which allows to set delay between campaigns (in days)
    and the amount of sending repetitions
    Args:
        None
    Returns:
        None
    """
    targets = file_reader.csv_reader('test_targets2.csv')
    Gophish_Instance = Gophish_runner.Gophish_Runner(config)
    Gophish_Instance.clear_all()

    Gophish_Instance.create_sending_profile('test')
    Gophish_Instance.create_landing_page('test', landing_page.generate_landing_page_html())

    if config["schedule"] == True:
        for target in targets:
            html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'], target['language'])
            Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject}", subject, html_email)
            Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], "proximus-ada-campaign@proton.me", target['position'])
            Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")

        for i in range(1, config["schedule_repetitions"]):
            for target in targets:
                html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'], target['language'])
                Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject} {i}", subject, html_email)
                Gophish_Instance.schedule_campaign(f"{target['name']} {target['last_name']} {subject} {i}", f"{target['name']} {target['last_name']} {subject} {i}", 'test', 'test', f"{target['name']} {target['last_name']}", i * config["schedule_delay"])

    else:
        for target in targets:
            html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'], target['language'])
            Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject}", subject, html_email)
            Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], "proximus-ada-campaign@proton.me", target['position'])
            Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")

main()
