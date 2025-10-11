# Contributing to JobSeek

Thank you for your interest in contributing to JobSeek! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear title and description
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the feature and its use case
- Explain why this feature would be useful
- Consider if it fits the project's scope

### Adding New Scrapers

To add support for a new ATS platform:

1. **Create the scraper file**
   ```bash
   touch jobseek/scrapers/new_ats.py
   ```

2. **Implement the scraper**
   ```python
   from jobseek.base_scraper import BaseScraper
   from jobseek.models import Job
   from typing import List

   class NewATSScraper(BaseScraper):
       def __init__(self, company_name: str):
           super().__init__(company_name)
           self.base_url = f"https://jobs.newats.com/{company_name}"
       
       def get_source_name(self) -> str:
           return "newats"
       
       def scrape(self) -> List[Job]:
           # Implement scraping logic
           jobs = []
           # ... fetch and parse job data ...
           return jobs
   ```

3. **Register the scraper**
   - Add to `jobseek/scrapers/__init__.py`
   - Add CLI command in `jobseek/cli.py`

4. **Add tests**
   - Create `tests/test_new_ats.py`
   - Test with mock data (no network calls)

5. **Update documentation**
   - Add to README.md
   - Update ARCHITECTURE.md
   - Add example companies

### Pull Request Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/JobSeek.git
   cd JobSeek
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add type hints
   - Write docstrings

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Update documentation**
   - Update README if adding features
   - Add docstrings to new functions
   - Update ARCHITECTURE.md if changing design

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Explain what changed and why

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/JobSeek.git
cd JobSeek

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=jobseek

# Run specific test file
pytest tests/test_models.py -v

# Run specific test
pytest tests/test_models.py::test_job_creation -v
```

### Code Style

We follow PEP 8 with some adjustments:

```bash
# Format code with black
black jobseek/ tests/

# Check with flake8
flake8 jobseek/ tests/ --max-line-length=100

# Type checking with mypy
mypy jobseek/
```

### Code Style Guidelines

- **Line length**: 100 characters max
- **Imports**: Group stdlib, third-party, and local imports
- **Docstrings**: Use Google style docstrings
- **Type hints**: Add type hints to all functions
- **Naming**: 
  - Classes: `PascalCase`
  - Functions: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private methods: `_leading_underscore`

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Test one thing per test
- Use fixtures for common setup

Example:
```python
def test_job_matches_filters_title():
    """Test filtering by title keywords."""
    job = Job(
        title="Senior Python Engineer",
        company="Test Corp",
        location="Remote",
        url="https://example.com/job/123",
        source="greenhouse",
    )
    
    assert job.matches_filters(title_keywords=["python"])
    assert not job.matches_filters(title_keywords=["java"])
```

## Project Structure

```
JobSeek/
├── jobseek/              # Main package
│   ├── __init__.py
│   ├── models.py         # Data models
│   ├── base_scraper.py   # Base scraper class
│   ├── cli.py           # CLI interface
│   ├── formatter.py     # Output formatting
│   └── scrapers/        # Individual scrapers
│       ├── __init__.py
│       ├── greenhouse.py
│       ├── lever.py
│       └── workday.py
├── tests/               # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   └── test_base_scraper.py
├── examples/            # Example scripts
├── requirements.txt     # Dependencies
├── setup.py            # Package setup
├── README.md           # Main documentation
└── ARCHITECTURE.md     # Architecture docs
```

## What to Work On

### Good First Issues

- Add more test coverage
- Improve error messages
- Add more example companies
- Improve documentation
- Fix typos

### Medium Complexity

- Add support for new ATS platforms
- Improve filtering logic
- Add new output formats
- Enhance CLI features

### Advanced

- Add caching layer
- Implement concurrent scraping
- Add database storage
- Create REST API wrapper
- Add JavaScript rendering support

## Review Process

Pull requests will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Documentation**: Is it well documented?
4. **Code Quality**: Is it clean and maintainable?
5. **Compatibility**: Does it work with existing code?

## Questions?

- Open an issue for questions
- Check existing documentation
- Look at examples in the codebase

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to JobSeek! 🎉
