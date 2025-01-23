from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, User, Group
import pandas as pd
import json

#with open('config.json', 'r') as f:
#    config = json.load(f)


class Gophish_Runner:
    """
    A class to interact with the Gophish API for managing phishing campaigns.
    Attributes:
        GOPHISH_API_KEY (str): The API key for Gophish.
        email_pass (str): The email password for the SMTP server.
        email_address (str): The email address for the SMTP server.
        host (str): The host for the SMTP server.
        port (int): The port for the SMTP server.
        gophish_api (Gophish): The Gophish API client.
        results (pd.DataFrame): The DataFrame to store campaign results.
    Methods:
        create_sending_profile(name):
            Creates a new sending profile in Gophish.
        clear_sending_profiles():
            Clears all sending profiles in Gophish.
        create_landing_page(name, html_str):
            Creates a new landing page in Gophish.
        clear_landing_pages():
            Clears all landing pages in Gophish.
        create_email_template(name, subject, html_str):
            Creates a new email template in Gophish.
        clear_email_templates():
            Clears all email templates in Gophish.
        create_group(name, first_name, last_name, email, position):
            Creates a new group in Gophish.
        clear_groups():
            Clears all groups in Gophish.
        create_campaign(name, template_name, page_name, sending_profile_name, group_name):
            Creates a new campaign in Gophish.
        clear_campaigns():
            Clears all campaigns in Gophish.
        get_results():
            Retrieves the results of all campaigns and stores them in a DataFrame.
        export_results(file_name='results.csv'):
            Exports the campaign results to a CSV file.
    """
    def __init__(self, config):
        self.GOPHISH_API_KEY = config["GOPHISH_API_KEY"]
        self.email_pass = config["email_pass"]
        self.email_address = config["email_address"]
        self.host = config["host"]
        self.port = config["port"]
        self.gophish_api = Gophish(self.GOPHISH_API_KEY, verify=False)
        self.results = None

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

    def get_results(self):
        self.results = None
        results_list = []
        for campaign in self.gophish_api.campaigns.get():
            res = campaign.results[0]
            results_list.append([res.first_name, res.last_name, res.position, res.status])
        df = pd.DataFrame(results_list, columns=['first_name', 'last_name', 'position', 'status'])
        
        self.results = df

    def export_results(self, file_name='results.csv'):
        self.results.to_csv(file_name, index=False)

    
