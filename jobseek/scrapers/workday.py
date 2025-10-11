"""
Workday ATS scraper.

Workday is an enterprise ATS platform.
Job boards vary by company but typically follow patterns like:
https://[company].wd1.myworkdayjobs.com/[site]/jobs
"""

from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import json
from jobseek.base_scraper import BaseScraper
from jobseek.models import Job, WorkMode, ExperienceLevel


class WorkdayScraper(BaseScraper):
    """Scraper for Workday job boards."""
    
    def __init__(self, company_name: str, workday_url: Optional[str] = None):
        """
        Initialize Workday scraper.
        
        Args:
            company_name: Company name for display
            workday_url: Full Workday jobs URL (required for Workday)
        """
        super().__init__(company_name)
        if not workday_url:
            raise ValueError("Workday URL is required for Workday scraper")
        self.workday_url = workday_url
        if not self.workday_url.startswith('http'):
            raise ValueError("Workday URL must be a complete URL")
    
    def get_source_name(self) -> str:
        """Get the source name."""
        return "workday"
    
    def scrape(self) -> List[Job]:
        """
        Scrape jobs from Workday board.
        
        Returns:
            List of Job objects
        """
        jobs = []
        
        try:
            # Workday uses an API endpoint
            # Try to parse the base URL to construct API endpoint
            if '/jobs' in self.workday_url:
                api_url = self.workday_url.rstrip('/jobs') + '/jobs'
            else:
                api_url = self.workday_url
            
            # Some Workday sites require specific headers
            headers = self.session.headers.copy()
            headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            })
            
            # Try API approach first (some Workday sites have JSON endpoints)
            try:
                response = self.session.get(api_url, headers=headers, timeout=10)
                if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    jobs = self._parse_json_response(data)
                    if jobs:
                        return jobs
            except (requests.exceptions.RequestException, ValueError):
                pass
            
            # Fall back to HTML scraping
            response = self.session.get(self.workday_url, timeout=10)
            response.raise_for_status()
            jobs = self._parse_html_response(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"Error scraping Workday for {self.company_name}: {e}")
        
        return jobs
    
    def _parse_json_response(self, data: dict) -> List[Job]:
        """Parse JSON response from Workday API."""
        jobs = []
        
        # Workday JSON structure varies, try common patterns
        job_listings = []
        if isinstance(data, dict):
            job_listings = data.get('jobPostings', [])
            if not job_listings:
                job_listings = data.get('jobs', [])
            if not job_listings:
                job_listings = data.get('results', [])
        elif isinstance(data, list):
            job_listings = data
        
        for job_data in job_listings:
            try:
                title = job_data.get('title', job_data.get('jobTitle', ''))
                location = job_data.get('location', job_data.get('locationName', 'Unknown'))
                
                # Construct job URL
                job_id = job_data.get('id', job_data.get('jobId', ''))
                job_url = job_data.get('url', '')
                if not job_url and job_id:
                    job_url = f"{self.workday_url}/{job_id}"
                
                description = job_data.get('description', job_data.get('jobDescription', ''))
                posted_date = job_data.get('postedOn', job_data.get('postingDate', None))
                
                # Detect work mode and experience level
                combined_text = f"{title} {location} {description[:200]}"
                work_mode = self._detect_work_mode(combined_text)
                experience_level = self._detect_experience_level(title)
                
                # Extract salary if available
                salary_min, salary_max, currency = self._extract_salary(description)
                
                # Extract keywords
                keywords = self._extract_keywords(title, description)
                
                # Generate LinkedIn URL
                linkedin_url = self._generate_linkedin_url(self.company_name, title)
                
                job = Job(
                    title=title,
                    company=self.company_name,
                    location=location,
                    url=job_url,
                    source=self.get_source_name(),
                    description=description[:500],
                    work_mode=work_mode,
                    experience_level=experience_level,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    salary_currency=currency,
                    posted_date=posted_date,
                    keywords=keywords,
                    linkedin_url=linkedin_url,
                )
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job: {e}")
                continue
        
        return jobs
    
    def _parse_html_response(self, html: str) -> List[Job]:
        """Parse HTML response from Workday board."""
        jobs = []
        soup = BeautifulSoup(html, 'lxml')
        
        # Workday boards often have job listings in specific structures
        # Try multiple selectors as Workday sites vary
        job_listings = soup.find_all('li', class_='css-1q2dra3')
        if not job_listings:
            job_listings = soup.find_all('div', attrs={'data-automation-id': 'compositeContainer'})
        if not job_listings:
            job_listings = soup.find_all('article')
        
        for listing in job_listings:
            try:
                # Find title
                title_elem = listing.find('a', attrs={'data-automation-id': 'jobTitle'})
                if not title_elem:
                    title_elem = listing.find('h3')
                if not title_elem:
                    title_elem = listing.find('a')
                
                if not title_elem:
                    continue
                
                title = title_elem.text.strip()
                job_url = title_elem.get('href', '')
                
                # Ensure full URL
                if job_url and not job_url.startswith('http'):
                    # Extract base URL from workday_url
                    base = '/'.join(self.workday_url.split('/')[:3])
                    job_url = base + job_url
                
                # Find location
                location_elem = listing.find('dd', attrs={'data-automation-id': 'location'})
                if not location_elem:
                    location_elem = listing.find('span', class_='location')
                location = location_elem.text.strip() if location_elem else 'Unknown'
                
                # Find posted date
                date_elem = listing.find('dd', attrs={'data-automation-id': 'postedOn'})
                posted_date = date_elem.text.strip() if date_elem else None
                
                # Detect work mode and experience level
                combined_text = f"{title} {location}"
                work_mode = self._detect_work_mode(combined_text)
                experience_level = self._detect_experience_level(title)
                
                # Generate LinkedIn URL
                linkedin_url = self._generate_linkedin_url(self.company_name, title)
                
                job = Job(
                    title=title,
                    company=self.company_name,
                    location=location,
                    url=job_url,
                    source=self.get_source_name(),
                    work_mode=work_mode,
                    experience_level=experience_level,
                    posted_date=posted_date,
                    linkedin_url=linkedin_url,
                )
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job listing: {e}")
                continue
        
        return jobs
