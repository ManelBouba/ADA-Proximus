from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import json

#with open('config.json', 'r') as f:
#    config = json.load(f)


class Gophish_Runner:
    def __init__(self, config):
        self.GOPHISH_API_KEY = config["GOPHISH_API_KEY"]
        self.email_pass = config["email_pass"]
        self.email_address = config["email_address"]
        self.host = config["host"]
        self.port = config["port"]
        self.gophish_api = Gophish(self.GOPHISH_API_KEY, verify=False)

    def create_sending_profile(self, name):    
        sending_profile = SMTP(
        name=name,
        from_address=self.email_address,
        from_name=name,
        reply_to_address=self.email_address,  
        host=self.host,  
        username=self.email_address,  
        password=self.email_pass,  
        port=587,  
        tls=True,  
        ssl=False,)

        self.gophish_api.smtp.post(sending_profile)

    def clear_sending_profiles(self):
        for sending_profile in self.gophish_api.smtp.get():
            self.gophish_api.smtp.delete(sending_profile.id)

    def create_landing_page(self, name, html_str):
        landing_page = Page(
        name=name,
        redirect_url="https://alkszo.github.io/security-training/landing_page",
        html=html_str, 
        capture_credentials=True,
        capture_passwords=True 
    )

        self.gophish_api.pages.post(landing_page)

    def clear_landing_pages(self):
        for slanding_page in self.gophish_api.pages.get():
            self.gophish_api.pages.delete(slanding_page.id)

    def create_email_template(self, name, subject, html_str):
        email_template = Template(
        name=name,
        subject=subject,
        html=html_str,    
    )

        self.gophish_api.templates.post(email_template)

    def clear_email_templates(self):
        for email_template in self.gophish_api.templates.get():
            self.gophish_api.templates.delete(email_template.id)

    def create_group(self, name, first_name, last_name, email, position):
        group = Group(
            name=name, 
            targets=[User(first_name=first_name, last_name=last_name, email=email, position=position)]
        )

        self.gophish_api.groups.post(group)

    def clear_groups(self):
        for group in self.gophish_api.groups.get():
            self.gophish_api.groups.delete(group.id)

    def create_campaign(self, name, template_name, page_name, sending_profile_name, group_name):
        campaign = Campaign(
        name=name,
        template=Template(name=template_name),
        page = Page(name=page_name),
        smtp=SMTP(name=sending_profile_name),
        groups=[Group(name=group_name)],
        url="http://127.0.0.1"
    )
    
        self.gophish_api.campaigns.post(campaign)

    def clear_campaigns(self):
        for campaign in self.gophish_api.campaigns.get():
            self.gophish_api.campaigns.delete(campaign.id)


    
