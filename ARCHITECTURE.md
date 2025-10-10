# Architecture Documentation

## System Overview

The Job Scraping Application is a modular, event-driven system that automatically collects, processes, and analyzes job postings from multiple sources.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions Workflow                       │
│                     (.github/workflows/daily-job-scrape.yml)        │
│                                                                       │
│  Trigger: Cron Schedule (Daily 9 AM UTC) OR Manual                  │
│  Runner: ubuntu-latest with Python 3.11                             │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          Main Orchestrator                           │
│                              (main.py)                               │
│                                                                       │
│  1. Setup logging (console + file)                                  │
│  2. Load configurations (companies.yaml, keywords.yaml)             │
│  3. Initialize all components                                       │
│  4. Orchestrate workflow                                            │
│  5. Generate summary report                                         │
└──┬──────────────┬──────────────┬──────────────┬────────────────────┘
   │              │              │              │
   │              │              │              │
   ▼              ▼              ▼              ▼
┌────────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
│  Fetchers  │ │Processor │ │ Reporter │ │    AI      │
│(fetchers.py)│(processor.py)│(reporter.py)│(ai_assistant.py)│
└────────────┘ └──────────┘ └──────────┘ └────────────┘
```

## Component Details

### 1. Configuration Layer

```
config/
├── companies.yaml     # ATS configurations
└── keywords.yaml      # Ranking and filtering rules
```

**companies.yaml Structure:**
```yaml
companies:
  - name: "Company Name"
    ats: "greenhouse|lever|ashby"
    board_token: "..."      # For Greenhouse
    board_url: "..."        # For Lever/Ashby
```

**keywords.yaml Structure:**
```yaml
keywords:
  high_priority: [...]      # +10 points
  medium_priority: [...]    # +5 points
  low_priority: [...]       # +2 points
preferred_skills: [...]     # +1 per match
preferred_locations: [...]  # +3 points
exclude_keywords: [...]     # Filter out
```

### 2. Fetchers Module (fetchers.py)

```
JobFetcherManager
    │
    ├── GreenhouseFetcher
    │   └── API: https://boards-api.greenhouse.io/v1/boards/{token}/jobs
    │
    ├── LeverFetcher
    │   └── API: https://api.lever.co/v0/postings/{company}
    │
    └── AshbyFetcher
        └── API: https://jobs.ashbyhq.com/{company}/api/jobs
```

**Responsibilities:**
- Fetch jobs from multiple ATS platforms
- Handle API errors gracefully
- Normalize data structure across platforms
- Return standardized job objects

**Normalized Job Object:**
```python
{
    'id': 'ats_company_jobid',
    'title': 'Job Title',
    'company': 'Company Name',
    'location': 'Location',
    'url': 'https://...',
    'description': 'Full description',
    'date_posted': 'ISO timestamp',
    'source': 'greenhouse|lever|ashby',
    'raw_data': {...}
}
```

### 3. Processor Module (processor.py)

```
JobProcessor
    │
    ├── normalize_location()      # Standardize location strings
    ├── should_exclude_job()      # Apply exclusion filters
    ├── calculate_job_score()     # Calculate relevance score
    ├── generate_job_hash()       # Create deduplication hash
    ├── deduplicate_jobs()        # Remove duplicates
    └── process_jobs()            # Main pipeline
```

**Processing Pipeline:**
1. **Normalization**: Standardize location (detect "Remote")
2. **Filtering**: Exclude jobs with unwanted keywords
3. **Scoring**: Calculate relevance based on:
   - Title matches (high/medium/low priority)
   - Skills in description
   - Preferred locations
   - Base score for all jobs
4. **Deduplication**: Hash-based on title + company
5. **Ranking**: Sort by score (descending)

**Scoring Algorithm:**
```
Score = Title_Match + Skills_Match + Location_Match + Base
where:
  Title_Match   = 10 (high) | 5 (medium) | 2 (low)
  Skills_Match  = 1 per skill + bonus (5 for 5+, 2 for 3+)
  Location_Match = 3 (if preferred)
  Base          = 1
```

### 4. Reporter Module (reporter.py)

```
JobReporter
    │
    ├── save_jobs_json()           # data/jobs_agg.json
    └── generate_markdown_report() # report/YYYY-MM-DD.md
```

**Output Formats:**

**JSON (data/jobs_agg.json):**
```json
{
  "generated_at": "ISO timestamp",
  "total_jobs": 123,
  "jobs": [
    { /* normalized job object */ },
    ...
  ]
}
```

**Markdown (report/YYYY-MM-DD.md):**
- Summary statistics
- Top companies
- Source breakdown
- Top 20 jobs (ranked)
- All jobs by company

### 5. GitHub Integration (github_integration.py)

```
GitHubIntegration
    │
    ├── commit_and_push_reports()    # Git operations
    ├── find_existing_issue()         # Search open issues
    ├── create_or_update_issue()      # API calls
    └── create_daily_digest_issue()   # Daily digest
```

**Operations:**
1. Configure git with bot credentials
2. Add and commit report files
3. Push to repository
4. Find or create "Daily Roles Digest" issue
5. Update issue with latest summary

### 6. AI Assistant Module (ai_assistant.py)

```
AIAssistant
    │
    ├── analyze_job_description()     # Extract key info
    ├── generate_resume_tips()        # Tailoring advice
    ├── generate_cover_letter_outline() # Cover letter structure
    ├── generate_interview_prep()     # Interview questions
    ├── analyze_top_jobs()            # Batch analysis
    └── generate_career_insights()    # Market trends
```

**Features (Optional - requires OPENAI_API_KEY):**
- Job description analysis
- Key responsibilities extraction
- Required/preferred skills identification
- Resume tailoring suggestions
- Cover letter outlines
- Interview preparation
- Career market insights

**Cost Optimization:**
- Uses GPT-3.5-turbo (cost-effective)
- Analyzes top 5 jobs only
- 2000 char description limit
- ~$0.01-0.05 per run

### 7. Main Orchestrator (main.py)

```
Execution Flow:
1. Setup logging
   └── Console (INFO) + File (DEBUG)

2. Load configurations
   └── companies.yaml + keywords.yaml

3. Initialize components
   └── Fetchers, Processor, Reporter, GitHub, AI

4. Fetch jobs
   └── For each company in config
       └── Fetch from appropriate ATS
       └── Handle errors, continue on failure

5. Process jobs
   └── Normalize → Filter → Score → Dedupe → Rank

6. Generate reports
   └── JSON + Markdown + AI insights (if enabled)

7. GitHub integration
   └── Commit/push + Create/update issue

8. Summary output
   └── Log statistics and file paths
```

## Data Flow

```
Companies Config → Fetchers → Raw Jobs
                                   │
                                   ▼
Keywords Config → Processor → Normalized/Scored Jobs
                                   │
                                   ▼
                   Reporter → JSON + Markdown
                                   │
                                   ▼
                   AI Assistant → Insights (optional)
                                   │
                                   ▼
                   GitHub Integration → Commit + Issue
```

## Error Handling Strategy

### Levels of Failure:

1. **Configuration Errors** (Fatal)
   - Missing config files → Exit with error
   - Invalid YAML syntax → Exit with error

2. **Network Errors** (Graceful)
   - API timeout → Log error, continue with other sources
   - DNS failure → Log error, continue
   - Rate limiting → Log error, continue

3. **Processing Errors** (Graceful)
   - Invalid job data → Skip job, continue
   - Scoring error → Use default score

4. **Output Errors** (Logged)
   - File write failure → Log error, may exit
   - Git push failure → Log warning, continue
   - Issue creation failure → Log warning, continue

5. **AI Errors** (Graceful Degradation)
   - Missing API key → Skip AI features
   - API error → Log warning, continue without AI

### Error Recovery:

```python
try:
    # API call
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
except RequestException as e:
    logger.error(f"API error: {e}")
    return []  # Empty result, continue processing
```

## Logging Strategy

### Log Levels:

- **DEBUG**: API requests, detailed processing steps
- **INFO**: High-level operations, job counts, success messages
- **WARNING**: Skipped operations, missing optional features
- **ERROR**: Failed operations that continue, API errors

### Log Outputs:

1. **Console** (INFO+): User-facing progress
2. **File** (DEBUG+): Full diagnostic information

### Log Locations:

```
logs/job_scraping_YYYY-MM-DD.log
```

## Extensibility Points

### Adding New ATS Platform:

1. Create fetcher class in `fetchers.py`:
```python
class NewATSFetcher:
    def fetch_jobs(self, board_url, company_name):
        # Implementation
        return normalized_jobs
```

2. Add to JobFetcherManager:
```python
self.new_ats = NewATSFetcher()
```

3. Update companies.yaml schema
4. Update documentation

### Adding New Ranking Criteria:

1. Add keywords to `keywords.yaml`
2. Update `calculate_job_score()` in processor.py
3. Document scoring changes

### Adding New Report Format:

1. Add method to JobReporter
2. Call from `generate_reports()`
3. Update main.py to handle new format

## Security Considerations

### Secrets Management:

- **GitHub Actions**: Use repository secrets
- **Local Development**: Use .env file (gitignored)
- **Never commit**: API keys, tokens, credentials

### API Rate Limiting:

- Use session objects for connection pooling
- Implement timeout (30s default)
- Graceful handling of rate limit errors

### Data Privacy:

- Job data is public information
- No PII collected or stored
- All data fetched from public APIs

## Performance Considerations

### Optimization Strategies:

1. **Parallel Fetching**: Could fetch from multiple companies in parallel (future enhancement)
2. **Caching**: Could cache results for debugging (future enhancement)
3. **Incremental Updates**: Could track last fetch time (future enhancement)

### Current Performance:

- ~10 companies: 10-30 seconds
- ~100-300 jobs: 1-2 seconds processing
- Report generation: <1 second
- Total runtime: <1 minute typically

## Testing Strategy

### Current Testing:

- Syntax validation (py_compile)
- Import testing
- Example script execution
- Manual output verification

### Recommended Testing (Future):

```python
# Unit tests
tests/
├── test_fetchers.py
├── test_processor.py
├── test_reporter.py
└── test_integration.py

# Integration test
tests/test_end_to_end.py
```

## Deployment

### GitHub Actions:

```yaml
Trigger: schedule (cron) or workflow_dispatch (manual)
Runner: ubuntu-latest
Python: 3.11
Dependencies: pip install -r requirements.txt
Secrets: GITHUB_TOKEN (auto), OPENAI_API_KEY (optional)
Permissions: contents:write, issues:write
```

### Local Development:

```bash
python main.py
```

## Monitoring

### Success Indicators:

- ✅ Jobs fetched > 0
- ✅ Reports generated
- ✅ Files committed to repo
- ✅ Issue created/updated

### Failure Indicators:

- ❌ Zero jobs from all sources
- ❌ File write errors
- ❌ Git push failures
- ❌ API authentication errors

### Logs to Monitor:

```bash
tail -f logs/job_scraping_*.log
```

## Future Enhancements

### Planned Features:

- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Email notifications
- [ ] Slack/Discord integration
- [ ] Job change detection
- [ ] Historical trend analysis
- [ ] More ATS platforms (Workday, iCIMS)
- [ ] Advanced filtering (salary, experience level)
- [ ] Resume matching score
- [ ] Application tracking

### Architecture Changes:

- [ ] Async fetching for better performance
- [ ] Plugin architecture for ATS fetchers
- [ ] Web dashboard for viewing results
- [ ] API endpoint for programmatic access

## References

- [Greenhouse API Documentation](https://developers.greenhouse.io/job-board.html)
- [Lever API Documentation](https://github.com/lever/postings-api)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
