import random
import google.generativeai as genai
import json


class PhishingEmailGenerator:
    def __init__(self, api_key, first_name, last_name, position):
        self.api_key = api_key
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.phishing_examples = [
            {"Reason": "Account Suspicious Activity", "Link": "http://fake-login.com", "Sender": "Security Team"},
            {"Reason": "Password Expiration Notice", "Link": "http://password-reset.com", "Sender": "IT Helpdesk"},
            {"Reason": "Document Signature Required", "Link": "http://sign-docs.com", "Sender": "Document Services"}
        ]
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def _generate_phishing_email(self):
        example = random.choice(self.phishing_examples)
        prompt = f"""
        Write a professional email from {example['Sender']} to {self.first_name} {self.last_name}, who is a {self.position}.
        Topic: {example['Reason']}.
        Include a link: {example['Link']}.
        """
        response = self.model.generate_content(prompt)
        response_text = response.text.replace("\n\n", "</p><p>").replace("\n", "<br>")
        return f"<p>{response_text}</p>", example['Reason']

    def generate_html_email(self):
        response_content, subject = self._generate_phishing_email()
        html_template = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Template</title>
            <style type="text/css">
                body {font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;}
                .email-container {width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #dddddd; border-radius: 8px; overflow: hidden;}
                .rs-border-c2 {border: 3px solid #5C2D91; padding: 20px;}
                .email-header {text-align: center; padding: 20px; background-color: #f4f4f4;}
                .email-header img {max-width: 150px; height: auto;}
                .email-body {padding: 30px; color: #333;}
                .button-container {text-align: center; margin-top: 30px;}
                .button {background-color: #5C2D91; color: #ffffff; padding: 18px 36px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block; font-size: 16px;}
                .email-footer {background-color: #f4f4f4; text-align: left; padding: 15px; font-size: 12px; color: #777;}
            </style>
        </head>
        <body>
        <div class="email-container rs-border-c2">
            <div class="email-header">
                <img alt="Company Logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Proximus_logo_2014.svg/1280px-Proximus_logo_2014.svg.png" />
            </div>
            <div class="email-body">
                {response_content}
            </div>
            <div class="button-container">
                <a class="button" href={{.URL}}>Click Here</a>
            </div>
        </div>
        <div class="email-footer">
            <p>You received this email as part of a <strong>Proximus Teams Notification</strong>.</p>
            <p>All rights reserved. <a href="#">&copy; 2025 Proximus</a> | <a href="#">Legal warnings</a> | <a href="#">Privacy</a></p>    
        </div>
        </body>
        </html>
        """
        html_email = html_template.replace("{response_content}", response_content)
        return html_email, subject


with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Example usage
email_generator = PhishingEmailGenerator(config["gemini_api_key"], "John", "Doe", "Manager")
html_email, subject = email_generator.generate_html_email()
