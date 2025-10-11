# JobSeek

A modular job scraper that aggregates job postings from multiple public Applicant Tracking Systems (ATS) like Greenhouse, Lever, and Workday.

## Features

- **Multi-Platform Support**: Scrape jobs from Greenhouse, Lever, and Workday ATS platforms
- **Advanced Filtering**: Filter by experience level, location, salary, work mode (remote/hybrid/on-site), and title keywords
- **LinkedIn Integration**: Automatically generates LinkedIn job search URLs for each position
- **Multiple Output Formats**: Export results as JSON, CSV, or formatted console output
- **Clean Architecture**: Modular, extensible design following software engineering best practices
- **Type Safety**: Fully typed Python code with dataclasses and enums

## Architecture

The project follows a clean, modular architecture:

```
jobseek/
├── models.py           # Core data models (Job, WorkMode, ExperienceLevel)
├── base_scraper.py     # Abstract base scraper with common functionality
├── scrapers/           # Individual ATS scrapers
│   ├── greenhouse.py   # Greenhouse ATS scraper
│   ├── lever.py        # Lever ATS scraper
│   └── workday.py      # Workday ATS scraper
├── formatter.py        # Output formatting (JSON, CSV, console)
└── cli.py             # Command-line interface
```

### Design Principles

1. **Extensibility**: Adding new scrapers is straightforward—just extend `BaseScraper`
2. **Single Responsibility**: Each module has a clear, focused purpose
3. **Open/Closed**: Open for extension (new scrapers), closed for modification
4. **Type Safety**: Uses Python type hints and dataclasses for robust code
5. **Error Handling**: Graceful handling of network errors and missing data

## Installation

```bash
# Clone the repository
git clone https://github.com/tsh39/JobSeek.git
cd JobSeek

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

### Basic Examples

**Scrape jobs from Greenhouse:**
```bash
jobseek greenhouse --company stripe
```

**Scrape jobs from Lever:**
```bash
jobseek lever --company netflix
```

**Scrape jobs from Workday:**
```bash
jobseek workday --company-name "Acme Corp" --url "https://acme.wd1.myworkdayjobs.com/careers"
```

### Advanced Filtering

**Filter by keywords in title:**
```bash
jobseek greenhouse --company airbnb --keywords python engineer backend
```

**Filter by location:**
```bash
jobseek lever --company github --location "San Francisco" "New York" remote
```

**Filter by work mode:**
```bash
jobseek greenhouse --company stripe --work-mode remote hybrid
```

**Filter by experience level:**
```bash
jobseek lever --company netflix --experience senior lead
```

**Filter by minimum salary:**
```bash
jobseek greenhouse --company stripe --min-salary 120000
```

**Combine multiple filters:**
```bash
jobseek greenhouse --company airbnb \
  --keywords python "machine learning" \
  --location remote \
  --work-mode remote \
  --experience senior \
  --min-salary 150000
```

### Output Formats

**Export to JSON:**
```bash
jobseek lever --company github --output results.json --format json
```

**Export to CSV:**
```bash
jobseek greenhouse --company stripe --output results.csv --format csv
```

**Verbose console output:**
```bash
jobseek lever --company netflix --verbose
```

## Output Structure

### JSON Format
```json
[
  {
    "title": "Senior Software Engineer",
    "company": "Example Corp",
    "location": "San Francisco, CA (Remote)",
    "url": "https://jobs.lever.co/example/abc123",
    "source": "lever",
    "description": "We are looking for...",
    "work_mode": "remote",
    "experience_level": "senior",
    "salary_min": 150000.0,
    "salary_max": 200000.0,
    "salary_currency": "USD",
    "posted_date": "2023-10-01",
    "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=...",
    "keywords": ["python", "aws", "kubernetes"]
  }
]
```

### CSV Format
Columns: title, company, location, url, source, work_mode, experience_level, salary_min, salary_max, salary_currency, posted_date, linkedin_url, keywords

## Supported ATS Platforms

### Greenhouse
- **URL Pattern**: `https://boards.greenhouse.io/[company]`
- **Features**: JSON API support, full job details
- **Examples**: Stripe, Airbnb, Pinterest

### Lever
- **URL Pattern**: `https://jobs.lever.co/[company]`
- **Features**: JSON API support, rich metadata
- **Examples**: Netflix, GitHub, Shopify

### Workday
- **URL Pattern**: Varies by company (e.g., `https://[company].wd1.myworkdayjobs.com/[site]`)
- **Features**: HTML scraping, structured data
- **Note**: Requires full URL due to varied patterns

## Adding New Scrapers

To add support for a new ATS platform:

1. Create a new file in `jobseek/scrapers/` (e.g., `my_ats.py`)
2. Extend the `BaseScraper` class
3. Implement required methods: `scrape()` and `get_source_name()`
4. Use helper methods from `BaseScraper` for common tasks

Example:
```python
from jobseek.base_scraper import BaseScraper
from jobseek.models import Job

class MyATSScraper(BaseScraper):
    def __init__(self, company_name: str):
        super().__init__(company_name)
        self.base_url = f"https://jobs.myats.com/{company_name}"
    
    def get_source_name(self) -> str:
        return "myats"
    
    def scrape(self) -> List[Job]:
        # Implement scraping logic
        jobs = []
        # ... scraping code ...
        return jobs
```

## Development

### Project Structure
- Clean separation of concerns
- Type hints throughout
- Docstrings for all public methods
- Modular design for easy testing

### Testing
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

## Technical Highlights

- **Object-Oriented Design**: Uses abstract base classes and inheritance
- **Data Classes**: Type-safe data models with `@dataclass`
- **Enumerations**: Type-safe enums for work modes and experience levels
- **Session Management**: Reusable HTTP sessions with proper headers
- **Error Handling**: Graceful degradation when services are unavailable
- **Pattern Matching**: Regex-based extraction of salary and other data
- **URL Construction**: Safe URL building and validation

## Use Cases

- **Job Seekers**: Aggregate and filter job postings from multiple companies
- **Recruiters**: Monitor job market and competitor postings
- **Researchers**: Analyze job market trends and salary data
- **Developers**: Learn web scraping and clean architecture patterns

## Limitations & Considerations

- **Rate Limiting**: Be respectful of ATS servers; add delays for large-scale scraping
- **Dynamic Content**: Some job boards use JavaScript rendering (may require Selenium)
- **Terms of Service**: Review and comply with each platform's ToS
- **Data Accuracy**: Salary and work mode detection is heuristic-based

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

Built to demonstrate clean architecture, extensibility, and software engineering best practices.

## Acknowledgments

- Greenhouse, Lever, and Workday for their public job boards
- Python community for excellent libraries (requests, beautifulsoup4)