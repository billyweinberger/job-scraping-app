"""
Reporter module for generating output files
"""
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class JobReporter:
    """Generates reports and output files"""
    
    def __init__(self, output_dir: str = "data", report_dir: str = "report"):
        self.output_dir = output_dir
        self.report_dir = report_dir
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)
    
    def save_jobs_json(self, jobs: List[Dict[str, Any]]) -> str:
        """Save jobs to JSON file"""
        output_file = os.path.join(self.output_dir, "jobs_agg.json")
        
        try:
            # Prepare data for JSON serialization
            json_data = {
                'generated_at': datetime.now().isoformat(),
                'total_jobs': len(jobs),
                'jobs': jobs
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(jobs)} jobs to {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"Error saving jobs to JSON: {e}")
            raise
    
    def generate_markdown_report(self, jobs: List[Dict[str, Any]]) -> str:
        """Generate markdown report for jobs"""
        today = datetime.now().strftime('%Y-%m-%d')
        report_file = os.path.join(self.report_dir, f"{today}.md")
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                # Header
                f.write(f"# Daily Job Scraping Report - {today}\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Summary\n\n")
                f.write(f"- **Total Jobs Found**: {len(jobs)}\n")
                
                # Count by company
                companies = {}
                for job in jobs:
                    company = job.get('company', 'Unknown')
                    companies[company] = companies.get(company, 0) + 1
                
                f.write(f"- **Companies**: {len(companies)}\n")
                f.write(f"- **Top Companies**:\n")
                for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]:
                    f.write(f"  - {company}: {count} jobs\n")
                
                f.write("\n")
                
                # Count by source
                sources = {}
                for job in jobs:
                    source = job.get('source', 'Unknown')
                    sources[source] = sources.get(source, 0) + 1
                
                f.write(f"- **Sources**:\n")
                for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                    f.write(f"  - {source}: {count} jobs\n")
                
                f.write("\n")
                
                # Top Jobs by Score
                f.write("## Top Job Opportunities\n\n")
                f.write("Jobs ranked by relevance score:\n\n")
                
                top_jobs = jobs[:20]  # Top 20 jobs
                
                for idx, job in enumerate(top_jobs, 1):
                    f.write(f"### {idx}. {job.get('title', 'N/A')}\n\n")
                    f.write(f"- **Company**: {job.get('company', 'N/A')}\n")
                    f.write(f"- **Location**: {job.get('location', 'N/A')}\n")
                    f.write(f"- **Relevance Score**: {job.get('score', 0):.1f}\n")
                    f.write(f"- **Apply**: [{job.get('url', 'N/A')}]({job.get('url', '#')})\n")
                    
                    # Truncate description
                    desc = job.get('description', 'N/A')
                    if len(desc) > 300:
                        desc = desc[:300] + '...'
                    # Remove HTML tags for markdown
                    import re
                    desc = re.sub('<[^<]+?>', '', desc)
                    desc = desc.replace('\n', ' ').strip()
                    
                    f.write(f"- **Description**: {desc}\n")
                    f.write("\n")
                
                # All Jobs by Company
                f.write("## All Jobs by Company\n\n")
                
                for company in sorted(companies.keys()):
                    company_jobs = [j for j in jobs if j.get('company') == company]
                    f.write(f"### {company} ({len(company_jobs)} jobs)\n\n")
                    
                    for job in company_jobs[:10]:  # Limit to 10 per company
                        f.write(f"- **{job.get('title', 'N/A')}** - {job.get('location', 'N/A')} ")
                        f.write(f"[Apply]({job.get('url', '#')}) (Score: {job.get('score', 0):.1f})\n")
                    
                    if len(company_jobs) > 10:
                        f.write(f"\n  _...and {len(company_jobs) - 10} more jobs_\n")
                    
                    f.write("\n")
                
                # Footer
                f.write("---\n\n")
                f.write("*Report generated by Job Scraping App*\n")
            
            logger.info(f"Generated markdown report: {report_file}")
            return report_file
        
        except Exception as e:
            logger.error(f"Error generating markdown report: {e}")
            raise
    
    def generate_reports(self, jobs: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate all reports"""
        return {
            'json': self.save_jobs_json(jobs),
            'markdown': self.generate_markdown_report(jobs)
        }
