"""
Job fetchers module for different ATS platforms
"""
import requests
import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class GreenhouseFetcher:
    """Fetcher for Greenhouse API"""
    
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Job-Scraping-App/1.0'
        })
    
    def fetch_jobs(self, board_token: str, company_name: str) -> List[Dict[str, Any]]:
        """Fetch jobs from Greenhouse board"""
        try:
            url = f"{self.BASE_URL}/{board_token}/jobs"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            jobs_data = response.json()
            jobs = jobs_data.get('jobs', [])
            
            normalized_jobs = []
            for job in jobs:
                normalized_jobs.append({
                    'id': f"gh_{board_token}_{job.get('id')}",
                    'title': job.get('title', ''),
                    'company': company_name,
                    'location': job.get('location', {}).get('name', ''),
                    'url': job.get('absolute_url', ''),
                    'description': job.get('content', ''),
                    'date_posted': job.get('updated_at', ''),
                    'source': 'greenhouse',
                    'raw_data': job
                })
            
            logger.info(f"Fetched {len(normalized_jobs)} jobs from Greenhouse for {company_name}")
            return normalized_jobs
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Greenhouse jobs for {company_name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching Greenhouse jobs for {company_name}: {e}")
            return []


class LeverFetcher:
    """Fetcher for Lever API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Job-Scraping-App/1.0'
        })
    
    def fetch_jobs(self, board_url: str, company_name: str) -> List[Dict[str, Any]]:
        """Fetch jobs from Lever API"""
        try:
            # Lever API typically uses format: https://api.lever.co/v0/postings/{company}
            response = self.session.get(board_url, timeout=30)
            response.raise_for_status()
            
            jobs = response.json()
            
            normalized_jobs = []
            for job in jobs:
                # Extract company from URL for ID generation
                company_slug = board_url.split('/')[-1]
                
                normalized_jobs.append({
                    'id': f"lever_{company_slug}_{job.get('id')}",
                    'title': job.get('text', ''),
                    'company': company_name,
                    'location': ', '.join([loc.get('name', '') for loc in job.get('categories', {}).get('location', [])]) if job.get('categories') else '',
                    'url': job.get('hostedUrl', ''),
                    'description': job.get('description', ''),
                    'date_posted': job.get('createdAt', ''),
                    'source': 'lever',
                    'raw_data': job
                })
            
            logger.info(f"Fetched {len(normalized_jobs)} jobs from Lever for {company_name}")
            return normalized_jobs
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Lever jobs for {company_name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching Lever jobs for {company_name}: {e}")
            return []


class AshbyFetcher:
    """Fetcher for Ashby GraphQL API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Job-Scraping-App/1.0'
        })
    
    def fetch_jobs(self, board_url: str, company_name: str) -> List[Dict[str, Any]]:
        """Fetch jobs from Ashby GraphQL API"""
        try:
            # Ashby uses a GraphQL endpoint
            # Example: https://jobs.ashbyhq.com/anthropic
            # We need to construct the API endpoint
            api_url = f"{board_url}/api/jobs"
            
            # Try REST endpoint first (some Ashby boards have REST API)
            response = self.session.get(api_url, timeout=30)
            response.raise_for_status()
            
            jobs_data = response.json()
            jobs = jobs_data.get('jobs', []) if isinstance(jobs_data, dict) else jobs_data
            
            normalized_jobs = []
            for job in jobs:
                # Extract company slug from URL
                company_slug = board_url.split('/')[-1]
                
                normalized_jobs.append({
                    'id': f"ashby_{company_slug}_{job.get('id', job.get('jobId', ''))}",
                    'title': job.get('title', ''),
                    'company': company_name,
                    'location': job.get('location', job.get('locationName', '')),
                    'url': job.get('jobUrl', f"{board_url}/{job.get('id', '')}"),
                    'description': job.get('description', job.get('descriptionHtml', '')),
                    'date_posted': job.get('publishedDate', job.get('createdAt', '')),
                    'source': 'ashby',
                    'raw_data': job
                })
            
            logger.info(f"Fetched {len(normalized_jobs)} jobs from Ashby for {company_name}")
            return normalized_jobs
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Ashby jobs for {company_name}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching Ashby jobs for {company_name}: {e}")
            return []


class JobFetcherManager:
    """Manages all job fetchers"""
    
    def __init__(self):
        self.greenhouse = GreenhouseFetcher()
        self.lever = LeverFetcher()
        self.ashby = AshbyFetcher()
    
    def fetch_all_jobs(self, companies_config: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fetch jobs from all configured companies"""
        all_jobs = []
        
        for company in companies_config:
            company_name = company.get('name')
            ats_type = company.get('ats', '').lower()
            
            logger.info(f"Fetching jobs for {company_name} ({ats_type})")
            
            try:
                if ats_type == 'greenhouse':
                    board_token = company.get('board_token')
                    if board_token:
                        jobs = self.greenhouse.fetch_jobs(board_token, company_name)
                        all_jobs.extend(jobs)
                
                elif ats_type == 'lever':
                    board_url = company.get('board_url')
                    if board_url:
                        jobs = self.lever.fetch_jobs(board_url, company_name)
                        all_jobs.extend(jobs)
                
                elif ats_type == 'ashby':
                    board_url = company.get('board_url')
                    if board_url:
                        jobs = self.ashby.fetch_jobs(board_url, company_name)
                        all_jobs.extend(jobs)
                
                else:
                    logger.warning(f"Unknown ATS type '{ats_type}' for {company_name}")
            
            except Exception as e:
                logger.error(f"Error processing {company_name}: {e}")
                continue
        
        logger.info(f"Total jobs fetched: {len(all_jobs)}")
        return all_jobs
