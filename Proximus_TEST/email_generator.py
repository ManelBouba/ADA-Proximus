import random
import google.generativeai as genai
import json


def generate_email_content(api_key, first_name, last_name, position):
    phishing_examples = [
    {"Reason": "Account Suspicious Activity", "Link": "http://fake-login.com", "Sender": "Security Team"},
    {"Reason": "Password Expiration Notice", "Link": "http://password-reset.com", "Sender": "IT Helpdesk"},
    {"Reason": "Document Signature Required", "Link": "http://sign-docs.com", "Sender": "Document Services"}
]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    example = random.choice(phishing_examples)
    prompt = f"""
    Write a professional email from {example['Sender']} to {first_name} {last_name}, who is a {position}.
    Topic: {example['Reason']}.
    Include a link: {example['Link']}.
    """
    response = model.generate_content(prompt)

    # Apply replacements to break the text into paragraphs and line breaks
    response = response.text.replace("\n\n", "</p><p>").replace("\n", "<br>")

    # Now wrap the response body with <p> tags if needed to make sure the text is inside paragraphs
    response_text = f"<p>{response}</p>"

    # HTML template
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
            <a class="button" href="http://yourlink.com">Click Here</a>
        </div>
    </div>
    <div class="email-footer">
        <p>You received this email as part of a <strong>Proximus Teams Notification</strong>.</p>
        <p>All rights reserved. <a href="#">&copy; 2025 Proximus</a> | <a href="#">Legal warnings</a> | <a href="#">Privacy</a></p>    
    </div>
    </body>
    </html>
    """

    # Insert the formatted content into the HTML template
    html_content = html_template.replace("{response_content}", response_text)

    # Print or save the final HTML
    print(html_content)

with open("config.json", "r") as config_file:
        config = json.load(config_file)

generate = generate_email_content(config["gemini_api_key"], "John", "Doe", "Manager")