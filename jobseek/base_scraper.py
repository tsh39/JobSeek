"""
Base scraper interface for all job board scrapers.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import requests
import re
from jobseek.models import Job, WorkMode, ExperienceLevel


class BaseScraper(ABC):
    """
    Abstract base class for all job scrapers.
    
    Provides common functionality and defines the interface that all
    scrapers must implement.
    """
    
    def __init__(self, company_name: Optional[str] = None):
        """
        Initialize the scraper.
        
        Args:
            company_name: Specific company to scrape jobs from (if applicable)
        """
        self.company_name = company_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    @abstractmethod
    def scrape(self) -> List[Job]:
        """
        Scrape jobs from the ATS.
        
        Returns:
            List of Job objects
        """
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of the ATS source.
        
        Returns:
            Source name (e.g., 'greenhouse', 'lever', 'workday')
        """
        pass
    
    def _detect_work_mode(self, text: str) -> WorkMode:
        """
        Detect work mode from job text.
        
        Args:
            text: Job title, description, or location text
            
        Returns:
            WorkMode enum value
        """
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['remote', 'work from home', 'wfh']):
            if any(keyword in text_lower for keyword in ['hybrid', 'flexible']):
                return WorkMode.HYBRID
            return WorkMode.REMOTE
        elif any(keyword in text_lower for keyword in ['hybrid', 'flexible']):
            return WorkMode.HYBRID
        elif any(keyword in text_lower for keyword in ['on-site', 'onsite', 'in-office', 'office']):
            return WorkMode.ONSITE
        
        return WorkMode.UNKNOWN
    
    def _detect_experience_level(self, text: str) -> ExperienceLevel:
        """
        Detect experience level from job text.
        
        Args:
            text: Job title or description text
            
        Returns:
            ExperienceLevel enum value
        """
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ['intern', 'internship']):
            return ExperienceLevel.INTERNSHIP
        elif any(keyword in text_lower for keyword in ['entry', 'junior', 'associate', 'graduate', 'jr.']):
            return ExperienceLevel.ENTRY
        elif any(keyword in text_lower for keyword in ['senior', 'sr.', 'staff']):
            return ExperienceLevel.SENIOR
        elif any(keyword in text_lower for keyword in ['lead', 'principal', 'architect']):
            return ExperienceLevel.LEAD
        elif any(keyword in text_lower for keyword in ['director', 'vp', 'vice president', 'chief', 'head of', 'executive']):
            return ExperienceLevel.EXECUTIVE
        elif any(keyword in text_lower for keyword in ['mid-level', 'intermediate']):
            return ExperienceLevel.MID
        
        # Default to mid if no specific level found
        return ExperienceLevel.MID
    
    def _extract_salary(self, text: str) -> tuple[Optional[float], Optional[float], str]:
        """
        Extract salary information from text.
        
        Args:
            text: Text containing salary information
            
        Returns:
            Tuple of (min_salary, max_salary, currency)
        """
        # Pattern for salary ranges like "$100,000 - $150,000" or "$100k-$150k"
        patterns = [
            r'\$(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)\s*-\s*\$(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)',
            r'\$(\d{1,3})k\s*-\s*\$?(\d{1,3})k',
            r'(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)\s*-\s*(\d{1,3}(?:,?\d{3})*(?:\.\d{2})?)\s*(?:USD|usd|\$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    min_sal = match.group(1).replace(',', '')
                    max_sal = match.group(2).replace(',', '')
                    
                    # Handle 'k' notation (thousands)
                    if 'k' in pattern:
                        min_sal = float(min_sal) * 1000
                        max_sal = float(max_sal) * 1000
                    else:
                        min_sal = float(min_sal)
                        max_sal = float(max_sal)
                    
                    return (min_sal, max_sal, "USD")
                except (ValueError, AttributeError):
                    continue
        
        return (None, None, "USD")
    
    def _extract_keywords(self, title: str, description: str) -> List[str]:
        """
        Extract relevant keywords from job title and description.
        
        Args:
            title: Job title
            description: Job description
            
        Returns:
            List of keywords
        """
        # Common tech keywords and skills
        tech_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node', 'django', 'flask', 'spring', 'aws', 'azure', 'gcp', 'docker',
            'kubernetes', 'sql', 'nosql', 'mongodb', 'postgresql', 'redis',
            'machine learning', 'ml', 'ai', 'data science', 'analytics',
            'frontend', 'backend', 'fullstack', 'full-stack', 'devops',
            'cloud', 'microservices', 'api', 'rest', 'graphql'
        ]
        
        text = (title + " " + description).lower()
        found_keywords = []
        
        for keyword in tech_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _generate_linkedin_url(self, company: str, title: str) -> Optional[str]:
        """
        Generate a LinkedIn job search URL for the position.
        
        Args:
            company: Company name
            title: Job title
            
        Returns:
            LinkedIn search URL or None
        """
        # Sanitize inputs for URL
        company_clean = company.replace(' ', '%20')
        title_clean = title.replace(' ', '%20')
        
        # Generate LinkedIn jobs search URL
        return f"https://www.linkedin.com/jobs/search/?keywords={title_clean}%20{company_clean}"
    
    def close(self):
        """Close the session."""
        self.session.close()
