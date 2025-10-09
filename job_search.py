import requests
import csv
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='job_search.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration (update with your RapidAPI key and search terms)
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')  # Set as environment variable in GitHub Actions
SEARCH_TERMS = ["Senior QA", "Dev Manager"]
LOCATION = "United States"  # Optional: specify location
RESULTS_PER_SEARCH = 10

def search_jobs(query, location=""):
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "country": "US" if location.lower() == "united states" else ""
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        jobs = data.get('data', [])
        logging.info(f"Found {len(jobs)} jobs for query: {query}")
        return jobs[:RESULTS_PER_SEARCH]
    except Exception as e:
        logging.error(f"Error searching for jobs with query '{query}': {e}")
        return []

def main():
    all_jobs = []
    for term in SEARCH_TERMS:
        jobs = search_jobs(term, LOCATION)
        for job in jobs:
            all_jobs.append({
                'Search Term': term,
                'Title': job.get('job_title', ''),
                'Company': job.get('employer_name', ''),
                'Location': job.get('job_city', '') + ', ' + job.get('job_state', ''),
                'URL': job.get('job_apply_link', ''),
                'Description': job.get('job_description', '')[:200] + '...' if job.get('job_description') else '',
                'Date Posted': job.get('job_posted_at_datetime_utc', '')
            })
    
    if all_jobs:
        filename = f"jobs_{datetime.now().strftime('%Y-%m-%d')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Search Term', 'Title', 'Company', 'Location', 'URL', 'Description', 'Date Posted']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_jobs)
        logging.info(f"Compiled {len(all_jobs)} jobs into {filename}")
        print(f"Job list compiled: {filename}")
    else:
        logging.info("No jobs found.")
        print("No jobs found.")

if __name__ == "__main__":
    main()