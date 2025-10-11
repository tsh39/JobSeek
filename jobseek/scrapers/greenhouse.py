"""
Greenhouse ATS scraper.

Greenhouse is a popular ATS used by many tech companies.
Job boards are typically at: https://boards.greenhouse.io/[company]
"""

from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from jobseek.base_scraper import BaseScraper
from jobseek.models import Job, WorkMode, ExperienceLevel


class GreenhouseScraper(BaseScraper):
    """Scraper for Greenhouse job boards."""
    
    def __init__(self, company_name: str):
        """
        Initialize Greenhouse scraper.
        
        Args:
            company_name: Company identifier used in Greenhouse URL
        """
        super().__init__(company_name)
        if not company_name:
            raise ValueError("Company name is required for Greenhouse scraper")
        self.base_url = f"https://boards.greenhouse.io/{company_name}"
    
    def get_source_name(self) -> str:
        """Get the source name."""
        return "greenhouse"
    
    def scrape(self) -> List[Job]:
        """
        Scrape jobs from Greenhouse board.
        
        Returns:
            List of Job objects
        """
        jobs = []
        
        try:
            # First, try to get the job board as JSON (many Greenhouse boards support this)
            json_url = f"{self.base_url}.json"
            response = self.session.get(json_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = self._parse_json_response(data)
            else:
                # Fall back to HTML scraping
                response = self.session.get(self.base_url, timeout=10)
                response.raise_for_status()
                jobs = self._parse_html_response(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"Error scraping Greenhouse for {self.company_name}: {e}")
        
        return jobs
    
    def _parse_json_response(self, data: dict) -> List[Job]:
        """Parse JSON response from Greenhouse API."""
        jobs = []
        
        job_listings = data.get('jobs', [])
        
        for job_data in job_listings:
            try:
                title = job_data.get('title', '')
                location = job_data.get('location', {}).get('name', 'Unknown')
                job_url = job_data.get('absolute_url', '')
                
                # Extract department and other metadata
                departments = job_data.get('departments', [])
                department = departments[0].get('name', '') if departments else ''
                
                # Detect work mode and experience level
                combined_text = f"{title} {location} {department}"
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
                    linkedin_url=linkedin_url,
                )
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job: {e}")
                continue
        
        return jobs
    
    def _parse_html_response(self, html: str) -> List[Job]:
        """Parse HTML response from Greenhouse board."""
        jobs = []
        soup = BeautifulSoup(html, 'lxml')
        
        # Greenhouse boards typically have job sections
        job_sections = soup.find_all('section', class_='level-0')
        
        for section in job_sections:
            job_listings = section.find_all('div', class_='opening')
            
            for listing in job_listings:
                try:
                    title_elem = listing.find('a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    job_url = title_elem.get('href', '')
                    
                    if not job_url.startswith('http'):
                        job_url = f"https://boards.greenhouse.io{job_url}"
                    
                    location_elem = listing.find('span', class_='location')
                    location = location_elem.text.strip() if location_elem else 'Unknown'
                    
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
                        linkedin_url=linkedin_url,
                    )
                    
                    jobs.append(job)
                    
                except Exception as e:
                    print(f"Error parsing job listing: {e}")
                    continue
        
        return jobs
