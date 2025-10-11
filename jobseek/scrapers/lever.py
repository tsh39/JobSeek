"""
Lever ATS scraper.

Lever is another popular ATS platform.
Job boards are typically at: https://jobs.lever.co/[company]
"""

from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from jobseek.base_scraper import BaseScraper
from jobseek.models import Job, WorkMode, ExperienceLevel


class LeverScraper(BaseScraper):
    """Scraper for Lever job boards."""
    
    def __init__(self, company_name: str):
        """
        Initialize Lever scraper.
        
        Args:
            company_name: Company identifier used in Lever URL
        """
        super().__init__(company_name)
        if not company_name:
            raise ValueError("Company name is required for Lever scraper")
        self.base_url = f"https://jobs.lever.co/{company_name}"
    
    def get_source_name(self) -> str:
        """Get the source name."""
        return "lever"
    
    def scrape(self) -> List[Job]:
        """
        Scrape jobs from Lever board.
        
        Returns:
            List of Job objects
        """
        jobs = []
        
        try:
            # Lever provides a JSON endpoint
            json_url = f"{self.base_url}?mode=json"
            response = self.session.get(json_url, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    jobs = self._parse_json_response(data)
                except ValueError:
                    # If JSON parsing fails, fall back to HTML
                    response = self.session.get(self.base_url, timeout=10)
                    response.raise_for_status()
                    jobs = self._parse_html_response(response.text)
            else:
                # Fall back to HTML scraping
                response = self.session.get(self.base_url, timeout=10)
                response.raise_for_status()
                jobs = self._parse_html_response(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"Error scraping Lever for {self.company_name}: {e}")
        
        return jobs
    
    def _parse_json_response(self, data: list) -> List[Job]:
        """Parse JSON response from Lever API."""
        jobs = []
        
        for job_data in data:
            try:
                title = job_data.get('text', '')
                location = job_data.get('categories', {}).get('location', 'Unknown')
                job_url = job_data.get('hostedUrl', '')
                description = job_data.get('description', '')
                
                # Get team/department
                team = job_data.get('categories', {}).get('team', '')
                commitment = job_data.get('categories', {}).get('commitment', '')
                
                # Detect work mode and experience level
                combined_text = f"{title} {location} {team} {commitment} {description[:200]}"
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
                    description=description[:500],  # Truncate for storage
                    work_mode=work_mode,
                    experience_level=experience_level,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    salary_currency=currency,
                    keywords=keywords,
                    linkedin_url=linkedin_url,
                )
                
                jobs.append(job)
                
            except Exception as e:
                print(f"Error parsing job: {e}")
                continue
        
        return jobs
    
    def _parse_html_response(self, html: str) -> List[Job]:
        """Parse HTML response from Lever board."""
        jobs = []
        soup = BeautifulSoup(html, 'lxml')
        
        # Lever boards have posting elements
        job_listings = soup.find_all('div', class_='posting')
        
        for listing in job_listings:
            try:
                title_elem = listing.find('h5')
                if not title_elem:
                    continue
                
                title = title_elem.text.strip()
                
                # Get the job URL
                link_elem = listing.find('a', class_='posting-btn-submit')
                if not link_elem:
                    link_elem = listing.find('a')
                
                job_url = link_elem.get('href', '') if link_elem else ''
                if not job_url.startswith('http'):
                    job_url = f"https://jobs.lever.co{job_url}"
                
                # Get location
                location_elem = listing.find('span', class_='sort-by-location')
                if not location_elem:
                    location_elem = listing.find('span', class_='posting-categories')
                location = location_elem.text.strip() if location_elem else 'Unknown'
                
                # Get commitment (Full-time, Part-time, etc.)
                commitment_elem = listing.find('span', class_='sort-by-commitment')
                commitment = commitment_elem.text.strip() if commitment_elem else ''
                
                # Detect work mode and experience level
                combined_text = f"{title} {location} {commitment}"
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
