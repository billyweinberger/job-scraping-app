# Quick Start Guide

Get started with the Job Scraping Application in 5 minutes.

## Prerequisites

- Python 3.11+
- Git
- GitHub account (for Actions)

## Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/billyweinberger/job-scraping-app.git
cd job-scraping-app

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import yaml, requests; print('✓ Dependencies installed')"
```

## Configuration (2 minutes)

### 1. Companies Configuration

Edit `config/companies.yaml` to add companies you want to track:

```yaml
companies:
  - name: "OpenAI"
    ats: "greenhouse"
    board_token: "openai"
```

**Finding company identifiers:**
- **Greenhouse**: Check company careers page URL (e.g., `boards.greenhouse.io/openai` → token: `openai`)
- **Lever**: Use API URL format: `https://api.lever.co/v0/postings/company-name`
- **Ashby**: Use jobs page URL: `https://jobs.ashbyhq.com/company-name`

### 2. Keywords Configuration

Edit `config/keywords.yaml` to customize job filtering:

```yaml
keywords:
  high_priority:
    - "Senior Software Engineer"
    - "Staff Engineer"
```

## Running (1 minute)

### Local Execution

```bash
python main.py
```

**Expected output:**
```
================================================================================
Starting Job Scraping Application
================================================================================
Loading configurations...
Loaded 10 companies
Fetching jobs from all sources...
Fetched 150 raw job postings
Processing jobs...
Processed to 120 unique, ranked jobs
Generating reports...
Reports generated successfully!
================================================================================
```

**Check outputs:**
```bash
# JSON output
cat data/jobs_agg.json

# Markdown report
cat report/2024-01-15.md

# Logs
cat logs/job_scraping_*.log
```

### GitHub Actions (Automated)

1. **Enable GitHub Actions**
   - Go to repository Settings → Actions → Allow all actions

2. **Configure secrets** (optional for AI features)
   - Go to Settings → Secrets → New repository secret
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key from https://platform.openai.com/api-keys

3. **Trigger workflow**
   - Go to Actions tab
   - Select "Daily Job Scraping"
   - Click "Run workflow"

4. **View results**
   - Check the `data/` and `report/` directories in your repository
   - Check GitHub Issues for "Daily Roles Digest"

## Quick Examples

### Example 1: Test with Example Script

```bash
python example_usage.py
```

This will:
- Process sample job data
- Generate test reports
- Show expected output format

### Example 2: Fetch from One Company

```python
from fetchers import GreenhouseFetcher

fetcher = GreenhouseFetcher()
jobs = fetcher.fetch_jobs("stripe", "Stripe")
print(f"Found {len(jobs)} jobs at Stripe")
```

### Example 3: Custom Processing

```python
import yaml
from processor import JobProcessor

# Load config
with open('config/keywords.yaml') as f:
    config = yaml.safe_load(f)

# Process jobs
processor = JobProcessor(config)
processed = processor.process_jobs(raw_jobs)

# Print top jobs
for job in processed[:5]:
    print(f"{job['title']} at {job['company']} - Score: {job['score']}")
```

## Common Commands

```bash
# Run main application
python main.py

# Run examples
python example_usage.py

# Check logs
tail -f logs/job_scraping_*.log

# Validate configuration
python -c "import yaml; yaml.safe_load(open('config/companies.yaml'))"

# Test imports
python -c "import fetchers, processor, reporter; print('✓ All modules working')"
```

## Output Structure

```
job-scraping-app/
├── data/
│   ├── jobs_agg.json         # All jobs with metadata
│   └── ai_insights.json      # AI analysis (if enabled)
├── report/
│   └── 2024-01-15.md         # Daily markdown report
└── logs/
    └── job_scraping_2024-01-15.log  # Execution logs
```

## Next Steps

After successful execution:

1. **Review outputs**
   - Check `data/jobs_agg.json` for structured data
   - Read `report/YYYY-MM-DD.md` for human-readable report
   - Review logs for any errors

2. **Customize**
   - Add more companies to `config/companies.yaml`
   - Adjust ranking weights in `config/keywords.yaml`
   - Modify scoring algorithm in `processor.py`

3. **Automate**
   - Enable GitHub Actions for daily runs
   - Set up email notifications (future feature)
   - Integrate with your job application tracker

4. **Enhance**
   - Enable AI features with OpenAI API key
   - Add more ATS platforms
   - Customize report formats

## Troubleshooting

### No jobs found
```bash
# Check network connectivity
python -c "import requests; requests.get('https://boards-api.greenhouse.io')"

# Verify company configuration
python -c "import yaml; print(yaml.safe_load(open('config/companies.yaml')))"
```

### Import errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### GitHub Actions not running
- Check repository permissions: Settings → Actions → Workflow permissions
- Ensure permissions are set to "Read and write permissions"

## Resources

- **Full Documentation**: See `README.md`
- **Setup Guide**: See `SETUP.md`
- **Architecture**: See `ARCHITECTURE.md`
- **Contributing**: See `CONTRIBUTING.md`

## Support

- GitHub Issues: https://github.com/billyweinberger/job-scraping-app/issues
- Documentation: All `.md` files in repository

## Summary Checklist

- [ ] Python 3.11+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Configuration files customized
- [ ] Local test run successful (`python main.py`)
- [ ] GitHub Actions enabled (optional)
- [ ] OpenAI API key configured (optional)
- [ ] Daily reports generating correctly

**You're all set! The application will now fetch, process, and rank jobs daily.** 🎉
