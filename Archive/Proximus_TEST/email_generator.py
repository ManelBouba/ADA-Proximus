import random
import google.generativeai as genai
import json
from datetime import datetime, timedelta


# Generate a random date and time for the email
current_date = datetime.now().date()


days_min = 2

days_max = 21


months_max = 3 * 30  

random_days = random.randint(days_min, days_max)
random_months = random.randint(0, months_max)

random_date = current_date + timedelta(days=random_days, weeks=random_months*4)

random_hour = random.randint(10, 16)
random_minute = random.randint(0, 59) 
random_datetime = datetime.combine(random_date, datetime.min.time()) + timedelta(hours=random_hour, minutes=random_minute)



def generate_email_content(api_key, first_name, last_name, position):
    phishing_examples = [
    {"Reason": "Document Signature Required", "Detailed_reason": "", "Link": "http://sign-docs.com", "Sender": "Document Services"},
    {"Reason": "Announcing the launch of our new internal collaboration platform.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Follow-up on action items from the digital transformation workshop.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Sign up for the upcoming seminar on cybersecurity best practices.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Share your thoughts: Help us improve Proximus as a great place to work.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Planned network maintenance: Impact on internal systems this weekend.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Our roadmap for sustainability: Key initiatives for 2025.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Stay secure: Best practices for managing passwords.", "Detailed_reason": "","Sender": "Vera"},
    {"Reason": "Save the date: Proximus Charity Run 2025.", "Detailed_reason": "Charity run organised by the receiver's employer which is Proximus","Sender": "Vera"},
    {"Reason": "Save the date: Proximus Tour de Namur Cyclo 2025.", "Detailed_reason": "As a proximus employee, you can take part to this sport event for free","Sender": "Vera"}
]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    example = random.choice(phishing_examples)
    prompt = f""""Compose a professional email from {example["Sender"]} to {first_name} {last_name}, who is a {position}, addressing the topic: {example["Reason"]}.

Structure the email as follows:

Opening: A friendly yet professional greeting.
Introduction: Briefly introduce the topic and why it is relevant to {first_name} {last_name}.
Explanation: Clearly and concisely explain the significance of {example["Reason"]}, and {example["Detailed_reason"]} in 2–3 sentences.
Closing: End with a polite and actionable request that encourages {first_name} {last_name} to respond or take the next step.
Tone and Style:

Professional, persuasive, and warm, with an optional hint of urgency (without being alarming).
Use natural and realistic language tailored to the recipient's role as a {position}.
Avoid overused words such as "crucial," "vital," "rare," or "urgent."
Requirements:

Use 75–100 words in total.
Avoid placeholders (e.g., '[Date and Time]') and special formatting (e.g., brackets '[]', '()', or '* **')..
If you include dates and times then use {random_datetime} as the date and time.
Avoid references to links or phrases like "click here."
Write only the body of the email, and ensure it is free of grammatical errors.
Use varied sentence structures and vocabulary to create a polished, engaging, and professional email.
Remeber that ou can change the subject line and the body of the email if you want to but Do not include the subject in the body email.
Signed, {example["Sender"]}.

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

    # Insert the formatted content into the HTML template
    html_email = html_template.replace("{response_content}", response_text)
    subject =example['Reason']
    return html_email, subject

"""
with open("config.json", "r") as config_file:
        config = json.load(config_file)

generate = generate_email_content(config["GEMINI_API_KEY"], "John", "Doe", "Manager")
"""