import random
import google.generativeai as genai
import json
# Predefined phishing examples
phishing_examples = [
    {"Reason": "Account Suspicious Activity", "Link": "http://fake-login.com", "Sender": "Security Team"},
    {"Reason": "Password Expiration Notice", "Link": "http://password-reset.com", "Sender": "IT Helpdesk"},
    {"Reason": "Document Signature Required", "Link": "http://sign-docs.com", "Sender": "Document Services"}
]

def generate_email_content(api_key, first_name, last_name, position):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    example = random.choice(phishing_examples)
    prompt = f"""
    Write a professional email from {example['Sender']} to {first_name} {last_name}, who is a {position}.
    Topic: {example['Reason']}.
    Include a link: {example['Link']}.
    """

    response = model.generate_content(prompt)
    print(response.text)
    return f"{example['Reason']}", response.text

with open("config.json", "r") as config_file:
        config = json.load(config_file)

generate = generate_email_content(config["gemini_api_key"], "John", "Doe", "Manager")