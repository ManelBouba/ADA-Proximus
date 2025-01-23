import Gophish_runner, landing_page, email_generator, file_reader
import json
import time
import pandas as pd
import urllib3
urllib3.disable_warnings()


with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    targets = file_reader.csv_reader('test_targets.csv')
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
        Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], config["email_address"], target['position'])
        Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")

    print('sending over')
    #time.sleep(120)
    #print('delay over')
    #Gophish_Instance.get_results()
    #Gophish_Instance.export_results()


main()
