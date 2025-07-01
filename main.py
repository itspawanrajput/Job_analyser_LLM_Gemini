
from scrapers.linkedin_scraper import search_linkedin
from analysis.job_analyzer import analyze_jobs

if __name__ == "__main__":
    # Path to your resume
    resume_path = "/Users/itspawanrajput/Desktop/Pawan_Rajput_AI_Data_Engineer.html"

    # Search for jobs
    jobs = search_linkedin("AI Data Engineer", "Remote")

    # Analyze and rank jobs
    if jobs:
        ranked_jobs = analyze_jobs(resume_path, jobs)
        print("\n--- Ranked Job Postings ---")
        for job in ranked_jobs:
            score_percent = job.get('relevancy_score', 0) * 100
            print(f"Relevancy: {score_percent:.2f}% - {job['title']} at {job['company']}")
            print(f"  Link: {job['link']}")
