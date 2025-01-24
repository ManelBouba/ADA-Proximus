from gophish import Gophish
from gophish.models import SMTP, Page, Template, Campaign, Group

class GophishAPI:
    def __init__(self, api_key, base_url):
        self.client = Gophish(api_key, base_url=base_url, verify=False)

    def create_email_template(self, subject, html_content):
        template = Template(name="Generated Email", subject=subject, html=html_content)
        return self.client.templates.post(template).id

    def create_landing_page(self, html_file):
        with open(html_file, "r") as file:
            html_content = file.read()
        page = Page(name="Phishing Landing Page", html=html_content)
        return self.client.pages.post(page).id

    def create_user_group(self, users):
        group = Group(name="Phishing Test Users", targets=users)
        return self.client.groups.post(group).id

    def create_campaign(self, campaign_name, template_id, page_id, smtp_profile_id, user_group_id):
        campaign = Campaign(
            name=campaign_name,
            template_id=template_id,
            page_id=page_id,
            smtp_id=smtp_profile_id,
            groups=[user_group_id]
        )
        return self.client.campaigns.post(campaign).id
