"""
Example companies using each ATS platform.

Use these as reference for testing the scrapers.
"""

GREENHOUSE_COMPANIES = [
    "stripe",
    "airbnb", 
    "coursera",
    "doordash",
    "gitlab",
    "pinterest",
    "robinhood",
    "coinbase",
    "grammarly",
    "twilio",
]

LEVER_COMPANIES = [
    "netflix",
    "github",
    "shopify",
    "lyft",
    "square",
    "figma",
    "notion",
    "cloudflare",
    "elastic",
    "reddit",
]

WORKDAY_EXAMPLES = [
    {
        "company": "Adobe",
        "url": "https://adobe.wd5.myworkdayjobs.com/external_experienced"
    },
    {
        "company": "Cisco",
        "url": "https://jobs.cisco.com/jobs/SearchJobs"
    },
    {
        "company": "Amazon",
        "url": "https://www.amazon.jobs/en/search"
    },
]


def print_examples():
    """Print example companies for reference."""
    print("=== Example Companies ===\n")
    
    print("Greenhouse (https://boards.greenhouse.io/[company]):")
    for company in GREENHOUSE_COMPANIES[:5]:
        print(f"  - {company}: https://boards.greenhouse.io/{company}")
    
    print("\nLever (https://jobs.lever.co/[company]):")
    for company in LEVER_COMPANIES[:5]:
        print(f"  - {company}: https://jobs.lever.co/{company}")
    
    print("\nWorkday (varies by company):")
    for example in WORKDAY_EXAMPLES[:3]:
        print(f"  - {example['company']}: {example['url']}")


if __name__ == "__main__":
    print_examples()
