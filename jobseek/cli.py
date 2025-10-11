"""
Command-line interface for JobSeek.
"""

import argparse
import sys
from typing import List, Optional
from jobseek.models import Job, WorkMode, ExperienceLevel
from jobseek.scrapers import GreenhouseScraper, LeverScraper, WorkdayScraper
from jobseek.formatter import OutputFormatter


def parse_work_modes(work_mode_strs: List[str]) -> List[WorkMode]:
    """Parse work mode strings to WorkMode enums."""
    work_modes = []
    for mode_str in work_mode_strs:
        try:
            work_modes.append(WorkMode[mode_str.upper()])
        except KeyError:
            print(f"Warning: Invalid work mode '{mode_str}'. Valid options: remote, hybrid, onsite")
    return work_modes


def parse_experience_levels(exp_strs: List[str]) -> List[ExperienceLevel]:
    """Parse experience level strings to ExperienceLevel enums."""
    levels = []
    for exp_str in exp_strs:
        try:
            levels.append(ExperienceLevel[exp_str.upper()])
        except KeyError:
            print(f"Warning: Invalid experience level '{exp_str}'. Valid options: internship, entry, mid, senior, lead, executive")
    return levels


def filter_jobs(
    jobs: List[Job],
    title_keywords: Optional[List[str]] = None,
    locations: Optional[List[str]] = None,
    work_modes: Optional[List[WorkMode]] = None,
    experience_levels: Optional[List[ExperienceLevel]] = None,
    min_salary: Optional[float] = None,
) -> List[Job]:
    """Filter jobs based on criteria."""
    filtered = []
    
    for job in jobs:
        if job.matches_filters(
            title_keywords=title_keywords,
            locations=locations,
            work_modes=work_modes,
            experience_levels=experience_levels,
            min_salary=min_salary,
        ):
            filtered.append(job)
    
    return filtered


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="JobSeek - Modular job scraper for multiple ATS platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape Greenhouse jobs from a company
  jobseek greenhouse --company stripe
  
  # Scrape Lever jobs with filters
  jobseek lever --company netflix --keywords python engineer --location "San Francisco"
  
  # Scrape Workday jobs
  jobseek workday --company-name "Example Corp" --url "https://example.wd1.myworkdayjobs.com/careers"
  
  # Use multiple filters
  jobseek greenhouse --company airbnb --work-mode remote hybrid --experience senior lead
  
  # Export to JSON
  jobseek lever --company github --output results.json --format json
        """
    )
    
    subparsers = parser.add_subparsers(dest='ats', help='ATS platform to scrape', required=True)
    
    # Greenhouse scraper
    greenhouse_parser = subparsers.add_parser('greenhouse', help='Scrape Greenhouse jobs')
    greenhouse_parser.add_argument('--company', required=True, help='Company identifier (from Greenhouse URL)')
    
    # Lever scraper
    lever_parser = subparsers.add_parser('lever', help='Scrape Lever jobs')
    lever_parser.add_argument('--company', required=True, help='Company identifier (from Lever URL)')
    
    # Workday scraper
    workday_parser = subparsers.add_parser('workday', help='Scrape Workday jobs')
    workday_parser.add_argument('--company-name', required=True, help='Company name for display')
    workday_parser.add_argument('--url', required=True, help='Full Workday jobs URL')
    
    # Common arguments for all scrapers
    for subparser in [greenhouse_parser, lever_parser, workday_parser]:
        # Filters
        subparser.add_argument('--keywords', nargs='+', help='Keywords to search in job title')
        subparser.add_argument('--location', nargs='+', help='Locations to filter by')
        subparser.add_argument('--work-mode', nargs='+', 
                             choices=['remote', 'hybrid', 'onsite'],
                             help='Work mode filter')
        subparser.add_argument('--experience', nargs='+',
                             choices=['internship', 'entry', 'mid', 'senior', 'lead', 'executive'],
                             help='Experience level filter')
        subparser.add_argument('--min-salary', type=float, help='Minimum salary filter')
        
        # Output options
        subparser.add_argument('--output', '-o', help='Output file path')
        subparser.add_argument('--format', '-f', 
                             choices=['json', 'csv', 'console'],
                             default='console',
                             help='Output format (default: console)')
        subparser.add_argument('--verbose', '-v', action='store_true',
                             help='Verbose output (shows descriptions and keywords)')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = None
    try:
        if args.ats == 'greenhouse':
            scraper = GreenhouseScraper(args.company)
        elif args.ats == 'lever':
            scraper = LeverScraper(args.company)
        elif args.ats == 'workday':
            scraper = WorkdayScraper(args.company_name, args.url)
        
        # Scrape jobs
        print(f"Scraping {args.ats} jobs...", file=sys.stderr)
        jobs = scraper.scrape()
        print(f"Found {len(jobs)} jobs", file=sys.stderr)
        
        # Apply filters
        work_modes = parse_work_modes(args.work_mode) if args.work_mode else None
        experience_levels = parse_experience_levels(args.experience) if args.experience else None
        
        filtered_jobs = filter_jobs(
            jobs,
            title_keywords=args.keywords,
            locations=args.location,
            work_modes=work_modes,
            experience_levels=experience_levels,
            min_salary=args.min_salary,
        )
        
        if len(filtered_jobs) < len(jobs):
            print(f"Filtered to {len(filtered_jobs)} jobs", file=sys.stderr)
        
        # Format and output results
        formatter = OutputFormatter()
        
        if args.format == 'json':
            output = formatter.to_json(filtered_jobs, args.output)
            if not args.output:
                print(output)
            else:
                print(f"Results written to {args.output}", file=sys.stderr)
        elif args.format == 'csv':
            output = formatter.to_csv(filtered_jobs, args.output)
            if not args.output:
                print(output)
            else:
                print(output, file=sys.stderr)
        else:  # console
            output = formatter.to_console(filtered_jobs, verbose=args.verbose)
            print(output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if scraper:
            scraper.close()


if __name__ == '__main__':
    main()
