# Changelog

All notable changes to the Job Scraping Application are documented in this file.

## [1.0.0] - 2024-10-09

### Added - Initial Release

#### Core Features
- **Multi-Platform Job Fetchers**
  - Greenhouse API integration (`https://boards-api.greenhouse.io`)
  - Lever API integration (`https://api.lever.co`)
  - Ashby GraphQL integration (`jobs.ashbyhq.com`)
  - Unified JobFetcherManager for orchestration

- **Data Processing Pipeline**
  - Job data normalization across different ATS platforms
  - Hash-based deduplication (MD5 of company + title)
  - Multi-factor ranking algorithm with configurable weights
  - Location normalization with Remote detection
  - Keyword-based job filtering and exclusion

- **Output Generation**
  - JSON output to `data/jobs_agg.json` with full metadata
  - Markdown daily reports to `report/YYYY-MM-DD.md`
  - Summary statistics (companies, sources, top jobs)
  - Jobs ranked by relevance score
  - Jobs grouped by company

- **GitHub Integration**
  - Automatic commit and push of generated reports
  - Create/update "Daily Roles Digest" GitHub issue
  - Top 10 opportunities in issue summary
  - Git configuration with bot credentials
  - Graceful handling of missing credentials

- **AI Integration (Optional)**
  - ChatGPT-powered job description analysis
  - Key responsibilities extraction
  - Required vs preferred skills identification
  - Resume tailoring suggestions
  - Cover letter outline generation
  - Interview preparation tips
  - Career market insights
  - Graceful degradation without API key
  - Cost optimization (GPT-3.5-turbo, top 5 jobs)

- **GitHub Actions Workflow**
  - Daily automated runs (9 AM UTC)
  - Python 3.11 runner on ubuntu-latest
  - Manual workflow dispatch option
  - Automatic artifact upload (30-day retention)
  - Proper permissions (contents: write, issues: write)

#### Configuration Files
- `config/companies.yaml` - 10 pre-configured companies
- `config/keywords.yaml` - Ranking and filtering rules
- `.env.example` - Environment variables template

#### Python Modules
- `main.py` - Main orchestrator with complete workflow
- `fetchers.py` - Multi-ATS job fetchers (373 lines)
- `processor.py` - Data processing pipeline (182 lines)
- `reporter.py` - Report generation (157 lines)
- `github_integration.py` - Git and issue management (200 lines)
- `ai_assistant.py` - ChatGPT integration (260 lines)
- `example_usage.py` - Usage examples and testing (134 lines)

#### Documentation
- `README.md` - Project overview and quick start (247 lines)
- `QUICKSTART.md` - 5-minute setup guide (230 lines)
- `SETUP.md` - Detailed configuration guide (305 lines)
- `ARCHITECTURE.md` - Technical documentation (479 lines)
- `CONTRIBUTING.md` - Development guidelines (280 lines)
- `LICENSE` - MIT License

#### Infrastructure
- `.github/workflows/daily-job-scrape.yml` - GitHub Actions workflow
- `.gitignore` - Ignore patterns for logs, cache, env files
- `requirements.txt` - Python dependencies (requests, PyYAML)

#### Error Handling & Logging
- Comprehensive error handling at all levels
- Graceful degradation on API failures
- Dual logging (console INFO + file DEBUG)
- Structured log files in `logs/` directory
- Context-rich error messages
- 30-second timeout for all API calls

#### Security
- GitHub secrets support for sensitive data
- Environment variable configuration
- No hardcoded credentials
- .gitignore for sensitive files
- Secure API key handling

### Technical Details

#### Scoring Algorithm
- Title keyword match: +10 (high priority) / +5 (medium) / +2 (low)
- Skills match: +1 per skill, +5 bonus for 5+ skills, +2 for 3+ skills
- Location preference: +3 for preferred locations
- Base score: +1 for all jobs

#### Deduplication Strategy
- Generate MD5 hash from normalized company + title
- Keep most detailed version when duplicates found
- Compare description length to determine best version

#### Performance Metrics
- Typical runtime: 30-60 seconds
- Handles 100-300 jobs per run
- Processing speed: ~1-2 seconds per 100 jobs
- AI analysis: ~10-20 seconds for top 5 jobs (optional)

### Dependencies

- Python 3.11+
- requests==2.31.0
- PyYAML==6.0.1

### Configuration

**Supported ATS Platforms:**
1. Greenhouse (board token)
2. Lever (board URL)
3. Ashby (board URL)

**Pre-configured Companies:**
- OpenAI (Greenhouse)
- Anthropic (Ashby)
- Stripe (Greenhouse)
- Airbnb (Greenhouse)
- Notion (Lever)
- Figma (Greenhouse)
- Scale AI (Ashby)
- Discord (Greenhouse)
- Databricks (Greenhouse)
- Ramp (Ashby)

### Usage

**Local:**
```bash
pip install -r requirements.txt
python main.py
```

**GitHub Actions:**
- Automatically runs daily at 9 AM UTC
- Manual trigger available in Actions tab

**With AI Features:**
- Configure `OPENAI_API_KEY` secret in repository

### Outputs

1. `data/jobs_agg.json` - All jobs with scores and metadata
2. `report/YYYY-MM-DD.md` - Daily human-readable report
3. `data/ai_insights.json` - AI analysis (if enabled)
4. `logs/job_scraping_YYYY-MM-DD.log` - Execution logs
5. GitHub Issue: "Daily Roles Digest" with top opportunities

### Extensibility

The modular architecture supports:
- Adding new ATS platforms (plugin-style)
- Customizing ranking algorithms
- Adding new report formats
- Integrating with other services
- Adding database storage

### Known Limitations

1. No rate limiting implementation (assumes API limits not reached)
2. No historical data storage (overwrites JSON each run)
3. No email notifications (future feature)
4. No database integration (file-based storage only)
5. AI features require OpenAI API key and have associated costs

### Future Enhancements

Planned for future releases:
- Database storage (SQLite/PostgreSQL)
- Email notifications
- Slack/Discord integration
- Job change detection
- Historical trend analysis
- More ATS platforms (Workday, iCIMS)
- Advanced filtering (salary, experience level)
- Resume matching score
- Application tracking
- Web dashboard

### Credits

- Architecture based on Mermaid diagram requirements
- Uses public APIs from Greenhouse, Lever, and Ashby
- OpenAI GPT-3.5-turbo for AI features (optional)
- GitHub Actions for automation

### License

MIT License - See LICENSE file for details

---

## Development History

### Commits

1. **Initial commit** - Repository setup
2. **Initial plan** - Project planning and structure
3. **Core implementation** - Fetchers, processor, reporter, GitHub integration, AI assistant
4. **Example script** - Usage examples and setup documentation
5. **Contributing guidelines** - Development guidelines and MIT license
6. **Architecture docs** - Comprehensive technical documentation
7. **Quick start guide** - Rapid onboarding guide

### Statistics

- **Total Files**: 26 files
- **Lines of Code**: 1,447 (Python + YAML + Workflows)
- **Lines of Documentation**: 1,491 (6 guides)
- **Commits**: 7
- **Duration**: Single implementation session

---

*This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.*
