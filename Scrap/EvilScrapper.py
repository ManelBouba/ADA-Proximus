import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Load the CSV file
file_path = 'linkedin_profiles.csv'
data = pd.read_csv(file_path)

# Define a function to scrape detailed information from a LinkedIn URL
def scrape_profile(url):
    try:
        # Make an HTTP request to fetch the page content
        COOKIES = {
        "li_at": "AQEDAVbNw14DmTWBAAABlHS7SaoAAAGUmMfNqk0AjMTQQc7rdzWXbYoI8U0QX5fB9Lo5XVe-BBKVQQjm7-ZOrFqHsvAMUdVcwQ83PZxgshC0v6e5cabr4jrk_ihi6oCmWFvhVejdpEN_Oy9UgCvtEh7i",
        "JSESSIONID": "ajax:8824062412405592960",
        "bcookie": "v=2&92b4c4d2-1b8f-41ec-821c-abf3e62b4ef3",
        "bscookie": "v=1&202501171446153d2283a4-1041-4f98-880c-d89e9a2819c3AQEnSUSEczShDKQJq5Scw-cYbLESOEiz",
        "lang": "v=2&lang=fr-fr",
        "lidc": "b=VB70:s=V:r=V:a=V:p=V:g=3805:u=2:x=1:i=1737448501:t=1737460287:v=2:sig=AQEQI8r7mIEojeeVnI_g4g4VUCD47smR",
        }
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "application/vnd.linkedin.normalized+json+2.1",
            "x-li-lang": "en_US",
            "x-li-track": "{\"clientVersion\":\"1.13.29149\",\"mpVersion\":\"1.13.29149\",\"osName\":\"web\",\"timezoneOffset\":1,\"timezone\":\"Europe/Brussels\",\"deviceFormFactor\":\"DESKTOP\",\"mpName\":\"voyager-web\",\"displayDensity\":1.5,\"displayWidth\":2256,\"displayHeight\":1504.5}",
            "csrf-token": "ajax:8824062412405592960",  # Replace with your CSRF token
            "x-restli-protocol-version": "2.0.0"
        }
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        response.raise_for_status()

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract specific details (adjust selectors as necessary for LinkedIn profiles)
        name = soup.find('h1', class_='text-heading-xlarge').get_text(strip=True) if soup.find('h1', class_='text-heading-xlarge') else None
        title = soup.find('div', class_='text-body-medium').get_text(strip=True) if soup.find('div', class_='text-body-medium') else None
        location = soup.find('span', class_='text-body-small').get_text(strip=True) if soup.find('span', class_='text-body-small') else None

        # Extract publications (example structure, may need adjustment)
        publications_section = soup.find('section', {'id': 'publications'})
        publications = []
        if publications_section:
            publications = [pub.get_text(strip=True) for pub in publications_section.find_all('li')]

        # Extract websites (example structure, may need adjustment)
        websites_section = soup.find('section', {'id': 'contact-info'})
        websites = []
        if websites_section:
            websites = [link['href'] for link in websites_section.find_all('a', href=True)]

        # Extract comments (if publicly available in activity sections)
        comments_section = soup.find('section', {'id': 'activity-comments'})
        comments = []
        if comments_section:
            comments = [comment.get_text(strip=True) for comment in comments_section.find_all('div', class_='comment-text')]

        # Return the extracted data
        return {
            'Name': name,
            'Title': title,
            'Location': location,
            'Publications': "|".join(publications) if publications else None,
            'Websites': "|".join(websites) if websites else None,
            'Comments': "|".join(comments) if comments else None,
            'URL': url
        }

    except Exception as e:
        # Handle errors and return None for problematic URLs
        print(f"Error scraping {url}: {e}")
        return {
            'Name': None,
            'Title': None,
            'Location': None,
            'Publications': None,
            'Websites': None,
            'Comments': None,
            'URL': url
        }

# List to store the scraped data
results = []

# Iterate through each URL in the CSV
for index, row in data.iterrows():
    profile_url = row['link']
    print(f"Scraping {profile_url}...")
    result = scrape_profile(profile_url)
    results.append(result)
    time.sleep(2)  # Pause to avoid overloading the server

# Save the results to a new CSV file
output_file = 'deep_data.csv'
scraped_data = pd.DataFrame(results)
scraped_data.to_csv(output_file, index=False)

print(f"Scraping complete. Data saved to {output_file}.")
