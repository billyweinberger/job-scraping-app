"""
AI Assistant module for job analysis using ChatGPT
"""
import os
import logging
from typing import List, Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


class AIAssistant:
    """ChatGPT integration for job analysis and career assistance"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
    
    def _call_chatgpt(self, messages: List[Dict[str, str]], max_tokens: int = 500) -> Optional[str]:
        """Make API call to ChatGPT"""
        if not self.api_key:
            logger.warning("OpenAI API key not configured - skipping AI analysis")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': max_tokens,
                'temperature': 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling ChatGPT API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in ChatGPT call: {e}")
            return None
    
    def analyze_job_description(self, job: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a job description and extract key information"""
        if not self.api_key:
            return None
        
        title = job.get('title', '')
        company = job.get('company', '')
        description = job.get('description', '')[:2000]  # Limit to avoid token limits
        
        messages = [
            {
                'role': 'system',
                'content': 'You are a career advisor analyzing job postings. Provide concise, actionable insights.'
            },
            {
                'role': 'user',
                'content': f"""Analyze this job posting and provide:
1. Key responsibilities (3-5 bullet points)
2. Required skills and qualifications
3. Nice-to-have skills
4. Company culture indicators
5. Red flags or concerns (if any)

Job Title: {title}
Company: {company}
Description: {description}

Provide the analysis in a structured format."""
            }
        ]
        
        analysis = self._call_chatgpt(messages, max_tokens=700)
        
        if analysis:
            return {
                'job_id': job.get('id'),
                'title': title,
                'company': company,
                'analysis': analysis
            }
        
        return None
    
    def generate_resume_tips(self, job: Dict[str, Any], user_skills: Optional[List[str]] = None) -> Optional[str]:
        """Generate resume tailoring tips for a specific job"""
        if not self.api_key:
            return None
        
        title = job.get('title', '')
        description = job.get('description', '')[:2000]
        
        skills_context = ""
        if user_skills:
            skills_context = f"\n\nCandidate's skills: {', '.join(user_skills)}"
        
        messages = [
            {
                'role': 'system',
                'content': 'You are a resume expert helping candidates tailor their resume for specific jobs.'
            },
            {
                'role': 'user',
                'content': f"""Based on this job posting, provide 5-7 specific tips on how to tailor a resume:

Job Title: {title}
Description: {description}{skills_context}

Focus on:
- Keywords to include
- Skills to emphasize
- Experience to highlight
- How to frame achievements"""
            }
        ]
        
        return self._call_chatgpt(messages, max_tokens=600)
    
    def generate_cover_letter_outline(self, job: Dict[str, Any]) -> Optional[str]:
        """Generate a cover letter outline for a job"""
        if not self.api_key:
            return None
        
        title = job.get('title', '')
        company = job.get('company', '')
        description = job.get('description', '')[:2000]
        
        messages = [
            {
                'role': 'system',
                'content': 'You are a career advisor helping candidates write compelling cover letters.'
            },
            {
                'role': 'user',
                'content': f"""Create a cover letter outline for this position:

Job Title: {title}
Company: {company}
Description: {description}

Provide:
1. Opening paragraph approach
2. Key points to address (3-4)
3. How to demonstrate fit
4. Closing paragraph approach"""
            }
        ]
        
        return self._call_chatgpt(messages, max_tokens=600)
    
    def generate_interview_prep(self, job: Dict[str, Any]) -> Optional[str]:
        """Generate interview preparation tips"""
        if not self.api_key:
            return None
        
        title = job.get('title', '')
        company = job.get('company', '')
        description = job.get('description', '')[:2000]
        
        messages = [
            {
                'role': 'system',
                'content': 'You are an interview coach preparing candidates for job interviews.'
            },
            {
                'role': 'user',
                'content': f"""Provide interview preparation guidance for this role:

Job Title: {title}
Company: {company}
Description: {description}

Include:
1. Likely interview questions (5-7)
2. Technical topics to review
3. Company research suggestions
4. Questions to ask the interviewer"""
            }
        ]
        
        return self._call_chatgpt(messages, max_tokens=800)
    
    def analyze_top_jobs(self, jobs: List[Dict[str, Any]], top_n: int = 5) -> Dict[str, Any]:
        """Analyze top N jobs and provide comprehensive insights"""
        if not self.api_key:
            logger.info("OpenAI API key not configured - skipping AI analysis")
            return {
                'enabled': False,
                'message': 'AI analysis disabled - configure OPENAI_API_KEY to enable'
            }
        
        analyses = []
        
        for job in jobs[:top_n]:
            logger.info(f"Analyzing job: {job.get('title')} at {job.get('company')}")
            
            analysis = self.analyze_job_description(job)
            if analysis:
                analyses.append(analysis)
        
        return {
            'enabled': True,
            'total_analyzed': len(analyses),
            'analyses': analyses
        }
    
    def generate_career_insights(self, jobs: List[Dict[str, Any]]) -> Optional[str]:
        """Generate overall career insights from job trends"""
        if not self.api_key or not jobs:
            return None
        
        # Aggregate job data
        titles = [job.get('title', '') for job in jobs[:20]]
        companies = list(set([job.get('company', '') for job in jobs[:20]]))
        
        messages = [
            {
                'role': 'system',
                'content': 'You are a career analyst providing insights on job market trends.'
            },
            {
                'role': 'user',
                'content': f"""Based on these job listings, provide career insights:

Job Titles: {', '.join(titles[:10])}
Companies hiring: {', '.join(companies[:10])}

Analyze:
1. Common skill requirements
2. Market trends
3. Career growth opportunities
4. Salary expectations (if inferable)
5. Recommendations for job seekers"""
            }
        ]
        
        return self._call_chatgpt(messages, max_tokens=800)
