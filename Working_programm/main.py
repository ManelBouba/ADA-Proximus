import Gophish_runner, landing_page, email_generator
import json
import time
import pandas as pd

with open('config.json', 'r') as f:
    config = json.load(f)

targets = [{'name':'Sofie', 'last_name':'Parys', 'position':'Sales & Segment Strategy Manager', 'email':config["email_address"]}, 
           {'name':'Saransh', 'last_name':'Goyal', 'position':'Strategy', 'email':config["email_address"]},
           {'name':'Kristiaan', 'last_name':'Vangeel', 'position':'Manager Network Deployment', 'email':config["email_address"]},
           {'name':'Cindy Joly', 'last_name':' Boyé ', 'position':'IT service delivery manager', 'email':config["email_address"]},
           {'name':'Zunaira', 'last_name':'Zahid', 'position':'Assistant Project Manager', 'email':config["email_address"]},
           {'name':'Carl', 'last_name':'Ringoet', 'position':'Product Owner', 'email':config["email_address"]},
           {'name':'Tom', 'last_name':'Logghe', 'position':'Team Manager eOperations', 'email':config["email_address"]},
           {'name':'Laetitia', 'last_name':'Bastin', 'position':'Account Manager', 'email':config["email_address"]},
           {'name':'Michel', 'last_name':'Simonart', 'position':'Head of Digital Ecosystems', 'email':config["email_address"]},
           {'name':'GEOFFREY', 'last_name':'HARING', 'position':'Service Delivery Manager', 'email':config["email_address"]}]

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

    print('loop is over')
    time.sleep(120)
    print('sleep over')
    Gophish_Instance.get_results()
    Gophish_Instance.export_results()


main()
