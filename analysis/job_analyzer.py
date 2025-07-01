
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_job_description(job_url):
    """Fetches the full job description from a LinkedIn job URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(job_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        description_div = soup.find('div', class_='show-more-less-html__markup')
        if description_div:
            return description_div.get_text(separator=' ', strip=True)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job description from {job_url}: {e}")
    return None

def analyze_jobs(resume_path, jobs):
    """Analyzes job descriptions against a resume and returns a ranked list."""
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            resume_text = f.read()
    except FileNotFoundError:
        print(f"Resume file not found at: {resume_path}")
        return []

    ranked_jobs = []
    for job in jobs:
        print(f"Analyzing job: {job['title']} at {job['company']}")
        job_description = get_job_description(job['link'])
        if job_description:
            # Create a TF-IDF Vectorizer
            vectorizer = TfidfVectorizer(stop_words='english')

            # Fit and transform the resume and job description
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])

            # Calculate cosine similarity
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            score = cosine_sim[0][0]

            job['relevancy_score'] = score
            ranked_jobs.append(job)

    # Sort jobs by relevancy score in descending order
    ranked_jobs.sort(key=lambda x: x.get('relevancy_score', 0), reverse=True)

    return ranked_jobs
