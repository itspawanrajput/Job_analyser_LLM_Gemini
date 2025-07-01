
import requests
from bs4 import BeautifulSoup

def search_indeed(query, location):
    """Searches Indeed for a given query and location."""
    print(f"Searching Indeed for '{query}' in '{location}'...")
    url = f"https://www.indeed.com/jobs?q={query}&l={location}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='job_seen_beacon'):
        title_element = job_card.find('h2', class_='jobTitle')
        company_element = job_card.find('span', class_='companyName')
        link_element = job_card.find('a', class_='jcs-JobTitle')

        if title_element and company_element and link_element:
            title = title_element.text.strip()
            company = company_element.text.strip()
            link = "https://www.indeed.com" + link_element['href']
            jobs.append({'title': title, 'company': company, 'link': link})

    print(f"Found {len(jobs)} jobs on Indeed.")
    return jobs
