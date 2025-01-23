import Gophish_runner, landing_page, email_generator, file_reader
import json
import time


with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    targets = file_reader.csv_reader('test_targets.csv')
    Gophish_Instance = Gophish_runner.Gophish_Runner(config)
    Gophish_Instance.clear_all()

    Gophish_Instance.create_sending_profile('test')
    Gophish_Instance.create_landing_page('test', landing_page.generate_landing_page_html())

    if config["schedule"] == True:
        print(config["schedule_delay"])
        for target in targets:
            html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'])
            Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject}", subject, html_email)
            Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], config["email_address"], target['position'])
            Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")

        for i in range(1, config["schedule_repetitions"]):
            for target in targets:
                html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'])
                Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject} {i}", subject, html_email)
                Gophish_Instance.schedule_campaign(f"{target['name']} {target['last_name']} {subject} {i}", f"{target['name']} {target['last_name']} {subject} {i}", 'test', 'test', f"{target['name']} {target['last_name']}", i * config["schedule_delay"])

    else:
        for target in targets:
            html_email, subject = email_generator.generate_email_content(config["GEMINI_API_KEY"], target["name"], target['last_name'], target['position'])
            Gophish_Instance.create_email_template(f"{target['name']} {target['last_name']} {subject}", subject, html_email)
            Gophish_Instance.create_group(f"{target['name']} {target['last_name']}", target["name"], target['last_name'], config["email_address"], target['position'])
            Gophish_Instance.create_campaign(f"{target['name']} {target['last_name']} {subject}", f"{target['name']} {target['last_name']} {subject}", 'test', 'test', f"{target['name']} {target['last_name']}")


main()
