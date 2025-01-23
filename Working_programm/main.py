import Gophish_runner, landing_page, email_generator
import json
import time
import pandas as pd
import urllib3
urllib3.disable_warnings()


with open('config.json', 'r') as f:
    config = json.load(f)

targets = [
    {'name': 'Wout', 'last_name': 'Van Aert', 'position': 'Contact Center Agent', 'email': 'wout.vanaert.visma@proton.me', 'language': 'french'},
    {'name': 'Remco', 'last_name': 'Evenepoel', 'position': 'Customer Service Specialist', 'email': 'remco.evenepoel.soudal@proton.me' , 'language': 'french'},
    {'name': 'Tadej', 'last_name': 'Pogacar', 'position': 'Sales Advisor', 'email': 'tadej.pogacar.uae@proton.me', 'language': 'dutch'},
    {'name': 'Arnaud', 'last_name': 'De Lie', 'position': 'B2B Sales Representative', 'email': 'arnaud.de.lie.lotto@proton.me', 'language': 'dutch'},
    {'name': 'Mathieu', 'last_name': 'Van Der Poel', 'position': 'Senior Legal Advisor', 'email': 'mathieu.vanderpoel.alpecin@proton.me', 'language': 'french'},
    {'name': 'Julian', 'last_name': 'Alaphilippe', 'position': 'Payroll Officer', 'email': 'julian.alaphilippe.tudor@proton.me', 'language': 'english'},
    {'name': 'Tom', 'last_name': 'Pidcock', 'position': 'Compensation & Benefits Specialist', 'email': 'tom.pidcock.q365@proton.me', 'language': 'english'},
    {'name': "Ben", 'last_name': "O'Connor", 'position': 'Finance Business Partner', 'email': 'ben.oconnor.decathlon@proton.me', 'language': 'french'},
    {'name': 'Jonas', 'last_name': 'Vingegaard', 'position': 'Finance Specialist', 'email': 'jonas.vinegegaard.visma@proton.me', 'language': 'english'},
    {'name': 'Victor', 'last_name': 'Campenaerts', 'position': 'Technical Dispatching', 'email': 'victor.campenaerts@proton.me', 'language': 'english'}
]


def main():
    Gophish_Instance = Gophish_runner.Gophish_Runner(config)
    Gophish_Instance.clear_sending_profiles()
    Gophish_Instance.clear_landing_pages()
    Gophish_Instance.clear_email_templates()
    Gophish_Instance.clear_groups()
    Gophish_Instance.clear_campaigns()

    Gophish_Instance.create_sending_profile('test')
    Gophish_Instance.create_landing_page('test', landing_page.generate_landing_page_html())

    for target in targets [:1]:
        html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'], target['language'])
        Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject}", subject, html_email)
        Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], target['email'], target['position'])
        Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")

    print('loop is over')
    time.sleep(120)
    print('sleep over')
    Gophish_Instance.get_results()
    Gophish_Instance.export_results()


main()
