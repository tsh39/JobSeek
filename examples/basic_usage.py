"""
Example script demonstrating JobSeek usage.

This script shows how to use the JobSeek library programmatically
to scrape jobs from multiple ATS platforms and apply filters.
"""

from jobseek.scrapers import GreenhouseScraper, LeverScraper
from jobseek.models import WorkMode, ExperienceLevel
from jobseek.formatter import OutputFormatter


def example_greenhouse():
    """Example: Scrape jobs from Greenhouse."""
    print("\n=== Greenhouse Example ===")
    
    # Initialize scraper for a company (e.g., "coursera" uses Greenhouse)
    scraper = GreenhouseScraper(company_name="coursera")
    
    try:
        # Scrape all jobs
        jobs = scraper.scrape()
        print(f"Found {len(jobs)} total jobs")
        
        # Filter for remote senior positions
        filtered = [
            job for job in jobs
            if job.matches_filters(
                title_keywords=["engineer", "developer"],
                work_modes=[WorkMode.REMOTE],
                experience_levels=[ExperienceLevel.SENIOR, ExperienceLevel.LEAD]
            )
        ]
        
        print(f"Found {len(filtered)} matching jobs")
        
        # Display results
        formatter = OutputFormatter()
        print(formatter.to_console(filtered[:5]))  # Show first 5
        
    finally:
        scraper.close()


def example_lever():
    """Example: Scrape jobs from Lever."""
    print("\n=== Lever Example ===")
    
    # Initialize scraper for a company (e.g., "netflix" uses Lever)
    scraper = LeverScraper(company_name="netflix")
    
    try:
        # Scrape all jobs
        jobs = scraper.scrape()
        print(f"Found {len(jobs)} total jobs")
        
        # Filter by keywords
        filtered = [
            job for job in jobs
            if job.matches_filters(
                title_keywords=["software", "engineer"]
            )
        ]
        
        print(f"Found {len(filtered)} matching jobs")
        
        # Export to JSON
        formatter = OutputFormatter()
        json_output = formatter.to_json(filtered, output_file="netflix_jobs.json")
        print("Exported to netflix_jobs.json")
        
    finally:
        scraper.close()


def example_multiple_sources():
    """Example: Scrape from multiple sources and combine."""
    print("\n=== Multiple Sources Example ===")
    
    all_jobs = []
    
    # Scrape from Greenhouse
    gh_scraper = GreenhouseScraper(company_name="stripe")
    try:
        gh_jobs = gh_scraper.scrape()
        all_jobs.extend(gh_jobs)
        print(f"Added {len(gh_jobs)} jobs from Greenhouse")
    finally:
        gh_scraper.close()
    
    # Scrape from Lever
    lever_scraper = LeverScraper(company_name="github")
    try:
        lever_jobs = lever_scraper.scrape()
        all_jobs.extend(lever_jobs)
        print(f"Added {len(lever_jobs)} jobs from Lever")
    finally:
        lever_scraper.close()
    
    # Filter combined results
    remote_jobs = [
        job for job in all_jobs
        if job.work_mode == WorkMode.REMOTE
    ]
    
    print(f"\nTotal jobs: {len(all_jobs)}")
    print(f"Remote jobs: {len(remote_jobs)}")
    
    # Export to CSV
    formatter = OutputFormatter()
    formatter.to_csv(all_jobs, output_file="combined_jobs.csv")
    print("Exported to combined_jobs.csv")


if __name__ == "__main__":
    print("JobSeek Examples")
    print("="*60)
    
    # Run examples (comment out as needed)
    example_greenhouse()
    # example_lever()
    # example_multiple_sources()
    
    print("\n" + "="*60)
    print("Examples complete!")
