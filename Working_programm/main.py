import Gophish_runner, landing_page, email_generator
import json

with open('config.json', 'r') as f:
    config = json.load(f)

targets = [{'name':'Joe', 'last_name':'Doe', 'position':'data janitor', 'email':config["email_address"]}, {'name':'Jane', 'last_name':'Dane', 'position':'data master', 'email':config["email_address"]}]

def main():
    Gophish_Instance = Gophish_runner.Gophish_Runner(config)
    Gophish_Instance.clear_sending_profiles()
    Gophish_Instance.clear_landing_pages()
    Gophish_Instance.clear_email_templates()
    Gophish_Instance.clear_groups()
    Gophish_Instance.clear_campaigns()

    Gophish_Instance.create_sending_profile('test')
    Gophish_Instance.create_landing_page('test', landing_page.generate_landing_page_html())

    for target in targets:
        html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'])
        Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject}", subject, html_email)
        Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], target['email'], target['position'])
        Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")

main()

