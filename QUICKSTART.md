# Quick Start Guide

Get started with JobSeek in 5 minutes!

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

## Your First Scrape

### 1. Scrape Jobs from Greenhouse

```bash
jobseek greenhouse --company stripe
```

This will scrape all jobs from Stripe's Greenhouse board and display them in your terminal.

### 2. Apply Filters

Filter for remote senior engineering positions:

```bash
jobseek greenhouse --company stripe \
  --keywords engineer \
  --work-mode remote \
  --experience senior
```

### 3. Export Results

Save results to a file:

```bash
# Export as JSON
jobseek lever --company netflix --output netflix_jobs.json --format json

# Export as CSV
jobseek lever --company netflix --output netflix_jobs.csv --format csv
```

## Common Use Cases

### Find Remote Python Jobs

```bash
jobseek greenhouse --company airbnb \
  --keywords python \
  --work-mode remote
```

### Find High-Paying Positions

```bash
jobseek lever --company github \
  --min-salary 150000 \
  --experience senior lead
```

### Compare Multiple Companies

```bash
# Scrape from multiple companies and combine
jobseek greenhouse --company stripe --output stripe.json --format json
jobseek lever --company netflix --output netflix.json --format json
```

## Using as a Python Library

```python
from jobseek.scrapers import GreenhouseScraper
from jobseek.models import WorkMode, ExperienceLevel

# Create scraper
scraper = GreenhouseScraper("stripe")

# Scrape jobs
jobs = scraper.scrape()

# Filter programmatically
remote_senior = [
    job for job in jobs
    if job.matches_filters(
        work_modes=[WorkMode.REMOTE],
        experience_levels=[ExperienceLevel.SENIOR]
    )
]

print(f"Found {len(remote_senior)} remote senior positions")

scraper.close()
```

## Running the Demo

See all features in action without network requests:

```bash
python demo.py
```

This demonstrates:
- Job filtering by multiple criteria
- Output formats (JSON, CSV, console)
- Job statistics and analysis

## Example Companies

### Greenhouse Companies

Try these companies that use Greenhouse:
- `stripe` - Financial infrastructure
- `airbnb` - Travel marketplace
- `gitlab` - DevOps platform
- `robinhood` - Trading platform
- `coinbase` - Cryptocurrency exchange

### Lever Companies

Try these companies that use Lever:
- `netflix` - Streaming service
- `github` - Code hosting platform
- `shopify` - E-commerce platform
- `figma` - Design tool
- `notion` - Productivity software

### Workday Companies

Workday URLs vary by company. Example format:

```bash
jobseek workday \
  --company-name "Adobe" \
  --url "https://adobe.wd5.myworkdayjobs.com/external_experienced"
```

## Tips & Tricks

### 1. Use Verbose Mode

Get more details about jobs:

```bash
jobseek greenhouse --company stripe --verbose
```

### 2. Combine Multiple Filters

Narrow down results:

```bash
jobseek lever --company netflix \
  --keywords "machine learning" python \
  --location "los angeles" remote \
  --work-mode remote hybrid \
  --experience mid senior
```

### 3. Pipe to Other Tools

Combine with standard Unix tools:

```bash
# Count jobs
jobseek greenhouse --company stripe --format json | jq length

# Extract specific fields
jobseek lever --company netflix --format json | jq '.[].title'

# Search in CSV
jobseek greenhouse --company stripe --format csv | grep -i python
```

### 4. Save Your Favorite Searches

Create shell aliases:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias jobseek-remote="jobseek greenhouse --company stripe --work-mode remote"
alias jobseek-python="jobseek lever --company netflix --keywords python"
```

## Troubleshooting

### "Company not found" or "No jobs returned"

- Verify the company identifier matches the URL slug
- Some companies may have moved to different ATS platforms
- Check if the company's job board is publicly accessible

### Network/Connection Errors

- Check your internet connection
- Some job boards may have rate limiting
- Try again after a few minutes

### Missing Dependencies

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Next Steps

- Read the full [README.md](README.md) for comprehensive documentation
- Check out [ARCHITECTURE.md](ARCHITECTURE.md) to understand the design
- Look at [examples/](examples/) for more code examples
- Run tests: `pytest tests/`

## Getting Help

- Check existing issues on GitHub
- Review the documentation
- Run `jobseek --help` for CLI options
- Run `jobseek [ats] --help` for platform-specific help

Happy job hunting! 🎯
