# Setup Guide

Complete setup instructions for the Job Scraping Application.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/billyweinberger/job-scraping-app.git
   cd job-scraping-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure companies and keywords**
   Edit `config/companies.yaml` and `config/keywords.yaml` to customize job sources and filtering.

4. **Run the application**
   ```bash
   python main.py
   ```

## Configuration

### Companies Configuration

Edit `config/companies.yaml` to add or remove companies to scrape:

```yaml
companies:
  - name: "Company Name"
    ats: "greenhouse"  # or "lever" or "ashby"
    board_token: "company-slug"  # for Greenhouse
    # OR
    board_url: "https://api.lever.co/v0/postings/company"  # for Lever/Ashby
```

**Supported ATS Types:**

1. **Greenhouse** (`ats: "greenhouse"`)
   - Use `board_token` (e.g., `"openai"`, `"stripe"`)
   - API: `https://boards-api.greenhouse.io/v1/boards/{token}/jobs`

2. **Lever** (`ats: "lever"`)
   - Use `board_url` (e.g., `"https://api.lever.co/v0/postings/notion"`)
   - API: Lever public postings API

3. **Ashby** (`ats: "ashby"`)
   - Use `board_url` (e.g., `"https://jobs.ashbyhq.com/anthropic"`)
   - API: Ashby job board API

### Keywords Configuration

Edit `config/keywords.yaml` to customize job filtering:

```yaml
keywords:
  high_priority:      # +10 points
    - "Senior Software Engineer"
  medium_priority:    # +5 points
    - "Software Engineer"
  low_priority:       # +2 points
    - "Junior Engineer"

preferred_skills:     # +1 point each
  - "Python"
  - "React"

preferred_locations:  # +3 points
  - "Remote"
  - "San Francisco"

exclude_keywords:     # Exclude jobs containing these
  - "Clearance Required"
```

## GitHub Actions Setup

### 1. Enable GitHub Actions

Ensure GitHub Actions is enabled in your repository settings.

### 2. Configure Secrets

Go to Settings → Secrets and variables → Actions → New repository secret:

- **GITHUB_TOKEN**: Automatically provided (no setup needed)
- **OPENAI_API_KEY**: (Optional) Your OpenAI API key for AI features
  - Get key from: https://platform.openai.com/api-keys
  - Without this, AI analysis features will be skipped

### 3. Workflow Configuration

The workflow is already configured in `.github/workflows/daily-job-scrape.yml`:

- **Schedule**: Daily at 9 AM UTC (customize the cron expression)
- **Manual trigger**: Available via Actions tab → Daily Job Scraping → Run workflow
- **Permissions**: Requires `contents: write` and `issues: write`

### 4. Test the Workflow

1. Go to Actions tab
2. Select "Daily Job Scraping"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Output Files

### 1. JSON Output (`data/jobs_agg.json`)

Contains all processed jobs with full metadata:

```json
{
  "generated_at": "2024-01-15T09:00:00",
  "total_jobs": 150,
  "jobs": [...]
}
```

### 2. Markdown Report (`report/YYYY-MM-DD.md`)

Human-readable daily report with:
- Summary statistics
- Top 20 jobs ranked by score
- All jobs grouped by company

### 3. AI Insights (`data/ai_insights.json`)

If OpenAI API key is configured, contains:
- Job description analyses
- Key responsibilities extracted
- Required skills identified

### 4. Logs (`logs/job_scraping_YYYY-MM-DD.log`)

Detailed execution logs including:
- Fetching progress
- Processing steps
- Errors and warnings
- API call details

## AI Features (Optional)

The application includes optional AI-powered features using ChatGPT:

### Available Features

1. **Job Analysis**: Extracts key information from job descriptions
2. **Resume Tips**: Suggests how to tailor your resume
3. **Cover Letter Outline**: Provides structure for cover letters
4. **Interview Prep**: Generates likely interview questions

### Enable AI Features

Set the `OPENAI_API_KEY` secret in your GitHub repository or as an environment variable:

```bash
export OPENAI_API_KEY="sk-..."
python main.py
```

### Cost Considerations

- Uses GPT-3.5-turbo by default (most cost-effective)
- Analyzes top 5 jobs per run
- Approximate cost: $0.01-0.05 per run
- Monitor usage at: https://platform.openai.com/usage

## Customization

### Change Scheduling

Edit `.github/workflows/daily-job-scrape.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Change this line
```

Common schedules:
- `'0 9 * * *'` - Daily at 9 AM UTC
- `'0 9 * * 1-5'` - Weekdays at 9 AM UTC
- `'0 */6 * * *'` - Every 6 hours

### Adjust Scoring

Modify the scoring logic in `processor.py`:

```python
def calculate_job_score(self, job: Dict[str, Any]) -> float:
    score = 0.0
    # Customize scoring logic here
    return score
```

### Add New Companies

1. Edit `config/companies.yaml`
2. Add company with appropriate ATS type
3. Workflow will automatically pick it up

### Customize Report Format

Modify `reporter.py`:

```python
def generate_markdown_report(self, jobs: List[Dict[str, Any]]) -> str:
    # Customize report format here
```

## Troubleshooting

### No jobs found

- Check company configuration in `config/companies.yaml`
- Verify ATS board tokens/URLs are correct
- Check logs for API errors

### GitHub Actions failures

- Verify repository permissions (contents: write, issues: write)
- Check workflow logs in Actions tab
- Ensure GITHUB_TOKEN is available (automatic)

### AI features not working

- Verify OPENAI_API_KEY is set as a secret
- Check API key is valid at https://platform.openai.com
- Review logs for API error messages

### Network errors

- Some ATS endpoints may have rate limiting
- Application handles errors gracefully and continues
- Check logs for specific API error messages

## Local Development

### Run in development mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug logging
python main.py

# Check logs
tail -f logs/job_scraping_*.log
```

### Test individual components

```bash
# Run example usage script
python example_usage.py

# Test a single fetcher
python -c "from fetchers import GreenhouseFetcher; f = GreenhouseFetcher(); print(f.fetch_jobs('stripe', 'Stripe'))"
```

## Support

For issues or questions:
1. Check existing GitHub Issues
2. Review logs in `logs/` directory
3. Open a new issue with logs and configuration

## License

MIT License - see LICENSE file for details
