# Contributing to Job Scraping Application

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in [GitHub Issues](https://github.com/billyweinberger/job-scraping-app/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Relevant logs or screenshots
   - Your environment (Python version, OS, etc.)

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check existing issues and discussions
2. Create a new issue with the `enhancement` label
3. Describe the feature and its use case
4. Explain how it would benefit users

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/job-scraping-app.git
   cd job-scraping-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and modular

Example:

```python
def fetch_jobs(self, board_token: str, company_name: str) -> List[Dict[str, Any]]:
    """Fetch jobs from Greenhouse board
    
    Args:
        board_token: Company's Greenhouse board identifier
        company_name: Human-readable company name
    
    Returns:
        List of normalized job dictionaries
    """
    # Implementation
```

### Logging

- Use appropriate log levels:
  - `logger.debug()` - Detailed diagnostic info
  - `logger.info()` - General informational messages
  - `logger.warning()` - Warning messages
  - `logger.error()` - Error messages
- Include context in log messages

### Error Handling

- Always handle exceptions gracefully
- Log errors with context
- Don't let one failure stop the entire process
- Return empty results rather than crashing

Example:

```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"Error fetching data: {e}")
    return []
```

## Adding New Features

### Adding a New ATS Fetcher

1. Create a new fetcher class in `fetchers.py`:

```python
class NewATSFetcher:
    """Fetcher for NewATS platform"""
    
    def fetch_jobs(self, board_url: str, company_name: str) -> List[Dict[str, Any]]:
        # Implementation
        pass
```

2. Add to `JobFetcherManager`:

```python
def __init__(self):
    self.new_ats = NewATSFetcher()

# Add to fetch_all_jobs method
elif ats_type == 'new_ats':
    jobs = self.new_ats.fetch_jobs(...)
```

3. Update configuration schema in `config/companies.yaml`
4. Update documentation in README.md and SETUP.md

### Adding New Ranking Criteria

1. Modify `JobProcessor.calculate_job_score()` in `processor.py`
2. Add new configuration options to `config/keywords.yaml`
3. Update documentation

### Adding New Report Formats

1. Add new method to `JobReporter` in `reporter.py`
2. Call it from `generate_reports()` method
3. Update `main.py` to handle new format

## Testing

### Manual Testing

Before submitting a PR:

1. **Test with sample data**
   ```bash
   python example_usage.py
   ```

2. **Test full execution**
   ```bash
   python main.py
   ```

3. **Check generated outputs**
   - Verify `data/jobs_agg.json` is valid JSON
   - Review `report/YYYY-MM-DD.md` for formatting
   - Check logs for errors

4. **Test error handling**
   - Test with invalid configuration
   - Test with network issues
   - Verify graceful degradation

### Testing Checklist

- [ ] Code follows style guidelines
- [ ] New features have docstrings
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate
- [ ] Configuration changes are documented
- [ ] README/SETUP.md updated if needed
- [ ] Manual testing completed
- [ ] No new warnings or errors in logs

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

   Commit message format:
   - Use present tense ("Add feature" not "Added feature")
   - Be descriptive but concise
   - Reference issues if applicable

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template:
     - What does this PR do?
     - Why is this change needed?
     - How was it tested?
     - Screenshots (if applicable)

## Pull Request Review

Your PR will be reviewed for:

- Code quality and style
- Functionality and correctness
- Error handling
- Documentation
- Testing coverage

Be prepared to:
- Answer questions about your implementation
- Make requested changes
- Update documentation

## Areas for Contribution

Here are some areas where contributions are especially welcome:

### High Priority

- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Improve error messages
- [ ] Add more ATS platform support
- [ ] Optimize API rate limiting

### Medium Priority

- [ ] Add more AI features
- [ ] Improve job matching algorithms
- [ ] Add email notifications
- [ ] Add database storage option
- [ ] Improve report visualizations

### Documentation

- [ ] Add more examples
- [ ] Create video tutorials
- [ ] Add troubleshooting guides
- [ ] Translate documentation

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome constructive feedback
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Publishing others' private information
- Other unprofessional conduct

## Questions?

If you have questions:

1. Check existing documentation (README.md, SETUP.md)
2. Search existing issues
3. Create a new issue with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
