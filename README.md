# Project Overview
This repository contains the code and resources for building an advanced phishing awareness platform for Proximus. The project helps employees better recognize phishing attempts and reduce security risks from social engineering. Using automation and AI, it creates realistic phishing campaigns, tracks employee responses, and provides training for those who need it most.

Key features include:

- Simulating Phishing Campaigns: Automatically send realistic phishing emails to employees.
- Tracking and Reporting: Monitor email opens, link clicks, phishing reports, and downloads via an interactive dashboard.
- Targeted Training: Provide tailored training for employees who frequently fall for phishing attempts.
- Secure Role-Based Access: Ensure secure data handling and role-specific features for admins and managers.
- This platform strengthens Proximus’s defenses against phishing attacks and improves employee security awareness.

## Description
### Data Analyst Tasks:
- Generate phishing emails with GenAI.
- Test email campaigns for accuracy.
- Build dashboards for campaign metrics using Gophish or similar tools.
- Collect training resources from the Cybersecurity Bootcamp team.
- Collaborate with DE for data formats and pipeline needs.
- Analyze campaign data to provide actionable insights.

### Data Engineer  Tasks:
- Develop APIs for email uploads and campaign triggers (FastAPI or similar).
- Enable both scheduled and manual campaigns.
- Retrieve and store campaign metrics for DA use.
- Ensure security and role-based access.
- Implement task scheduling using Python schedulers (e.g., sched).

## Installation

1. Clone the Repository:

```bash
git clone https://github.com/ManelBouba/ADA-Proximus.git
cd ADA-Proximus
```
2. Install Requirements:
Make sure you have Python 3.8 or later installed. Then, install the required packages:
```bash
pip install -r requirements.txt 
```
3.  Verify GoPhish Installation: Ensure you have GoPhish installed and configured before running the application. Refer to the GoPhish documentation for setup details.
4. Run the Application:
Depending on your application structure, provide commands, e.g.,: ```bash
python main.py
```
