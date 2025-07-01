
import requests
from bs4 import BeautifulSoup

def search_linkedin(query, location):
    """Searches LinkedIn for a given query and location."""
    print(f"Searching LinkedIn for '{query}' in '{location}'...")
    url = f"https://www.linkedin.com/jobs/search?keywords={query}&location={location}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='base-card'):
        title_element = job_card.find('h3', class_='base-search-card__title')
        company_element = job_card.find('h4', class_='base-search-card__subtitle')
        link_element = job_card.find('a', class_='base-card__full-link')

        if title_element and company_element and link_element:
            title = title_element.text.strip()
            company = company_element.text.strip()
            link = link_element['href']
            jobs.append({'title': title, 'company': company, 'link': link})

    print(f"Found {len(jobs)} jobs on LinkedIn.")
    return jobs
