"""
Job data processing module - normalization, deduplication, and ranking
"""
import logging
from typing import List, Dict, Any
from datetime import datetime
import hashlib
import re

logger = logging.getLogger(__name__)


class JobProcessor:
    """Processes job data - normalizes, deduplicates, and ranks"""
    
    def __init__(self, keywords_config: Dict[str, Any]):
        self.keywords_config = keywords_config
        self.high_priority_keywords = keywords_config.get('keywords', {}).get('high_priority', [])
        self.medium_priority_keywords = keywords_config.get('keywords', {}).get('medium_priority', [])
        self.low_priority_keywords = keywords_config.get('keywords', {}).get('low_priority', [])
        self.preferred_skills = keywords_config.get('preferred_skills', [])
        self.preferred_locations = keywords_config.get('preferred_locations', [])
        self.exclude_keywords = keywords_config.get('exclude_keywords', [])
    
    def normalize_location(self, location: str) -> str:
        """Normalize location string"""
        if not location:
            return "Unknown"
        
        location = location.strip()
        
        # Check for remote patterns
        if any(remote_term in location.lower() for remote_term in ['remote', 'anywhere', 'distributed']):
            return "Remote"
        
        return location
    
    def should_exclude_job(self, job: Dict[str, Any]) -> bool:
        """Check if job should be excluded based on keywords"""
        text_to_check = f"{job.get('title', '')} {job.get('description', '')}".lower()
        
        for exclude_kw in self.exclude_keywords:
            if exclude_kw.lower() in text_to_check:
                logger.info(f"Excluding job '{job.get('title')}' - contains '{exclude_kw}'")
                return True
        
        return False
    
    def calculate_job_score(self, job: Dict[str, Any]) -> float:
        """Calculate relevance score for a job posting"""
        score = 0.0
        
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        location = job.get('location', '').lower()
        
        # Title keyword matching
        for keyword in self.high_priority_keywords:
            if keyword.lower() in title:
                score += 10.0
                break
        
        for keyword in self.medium_priority_keywords:
            if keyword.lower() in title:
                score += 5.0
                break
        
        for keyword in self.low_priority_keywords:
            if keyword.lower() in title:
                score += 2.0
                break
        
        # Preferred skills matching (in description)
        skills_matched = 0
        for skill in self.preferred_skills:
            if skill.lower() in description or skill.lower() in title:
                skills_matched += 1
                score += 1.0
        
        # Bonus for multiple skills
        if skills_matched >= 5:
            score += 5.0
        elif skills_matched >= 3:
            score += 2.0
        
        # Location preference
        for pref_loc in self.preferred_locations:
            if pref_loc.lower() in location:
                score += 3.0
                break
        
        # Boost for certain companies (can be configured later)
        # For now, give slight boost to all fetched jobs
        score += 1.0
        
        return score
    
    def generate_job_hash(self, job: Dict[str, Any]) -> str:
        """Generate a hash for deduplication based on title and company"""
        # Normalize title and company for consistent hashing
        title = job.get('title', '').lower().strip()
        company = job.get('company', '').lower().strip()
        
        # Remove common variations
        title = re.sub(r'\s+', ' ', title)
        title = re.sub(r'[^\w\s]', '', title)
        
        hash_string = f"{company}:{title}"
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def deduplicate_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate job postings"""
        seen_hashes = {}
        unique_jobs = []
        
        for job in jobs:
            job_hash = self.generate_job_hash(job)
            
            if job_hash not in seen_hashes:
                seen_hashes[job_hash] = job
                unique_jobs.append(job)
            else:
                # Keep the one with more information or higher score
                existing = seen_hashes[job_hash]
                if len(job.get('description', '')) > len(existing.get('description', '')):
                    # Replace with more detailed version
                    seen_hashes[job_hash] = job
                    unique_jobs = [j for j in unique_jobs if self.generate_job_hash(j) != job_hash]
                    unique_jobs.append(job)
        
        logger.info(f"Deduplicated {len(jobs)} jobs to {len(unique_jobs)} unique jobs")
        return unique_jobs
    
    def process_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Main processing pipeline"""
        logger.info(f"Processing {len(jobs)} jobs")
        
        processed_jobs = []
        
        for job in jobs:
            # Normalize location
            job['location'] = self.normalize_location(job.get('location', ''))
            
            # Check if should be excluded
            if self.should_exclude_job(job):
                continue
            
            # Calculate score
            job['score'] = self.calculate_job_score(job)
            
            # Add processing metadata
            job['processed_at'] = datetime.now().isoformat()
            
            processed_jobs.append(job)
        
        # Deduplicate
        processed_jobs = self.deduplicate_jobs(processed_jobs)
        
        # Sort by score (highest first)
        processed_jobs.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        logger.info(f"Processing complete: {len(processed_jobs)} jobs after filtering and ranking")
        return processed_jobs
