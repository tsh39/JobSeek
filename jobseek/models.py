"""
Core data models for job postings.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class WorkMode(Enum):
    """Work mode enumeration."""
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    UNKNOWN = "unknown"


class ExperienceLevel(Enum):
    """Experience level enumeration."""
    INTERNSHIP = "internship"
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"
    UNKNOWN = "unknown"


@dataclass
class Job:
    """
    Represents a job posting.
    
    Attributes:
        title: Job title
        company: Company name
        location: Job location
        url: Link to the original job posting
        description: Job description text
        work_mode: Remote, hybrid, or onsite
        experience_level: Required experience level
        salary_min: Minimum salary (if available)
        salary_max: Maximum salary (if available)
        salary_currency: Currency for salary (default: USD)
        posted_date: Date the job was posted
        source: ATS source (greenhouse, lever, workday, etc.)
        linkedin_url: LinkedIn job posting URL (if available)
        keywords: List of relevant keywords extracted from the job
    """
    title: str
    company: str
    location: str
    url: str
    source: str
    description: str = ""
    work_mode: WorkMode = WorkMode.UNKNOWN
    experience_level: ExperienceLevel = ExperienceLevel.UNKNOWN
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "USD"
    posted_date: Optional[str] = None
    linkedin_url: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert job to dictionary format."""
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "source": self.source,
            "description": self.description,
            "work_mode": self.work_mode.value,
            "experience_level": self.experience_level.value,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_currency": self.salary_currency,
            "posted_date": self.posted_date,
            "linkedin_url": self.linkedin_url,
            "keywords": self.keywords,
        }
    
    def matches_filters(
        self,
        title_keywords: Optional[List[str]] = None,
        locations: Optional[List[str]] = None,
        work_modes: Optional[List[WorkMode]] = None,
        experience_levels: Optional[List[ExperienceLevel]] = None,
        min_salary: Optional[float] = None,
    ) -> bool:
        """
        Check if job matches given filters.
        
        Args:
            title_keywords: Keywords to match in job title
            locations: Locations to match
            work_modes: Work modes to match
            experience_levels: Experience levels to match
            min_salary: Minimum salary threshold
            
        Returns:
            True if job matches all provided filters
        """
        # Check title keywords
        if title_keywords:
            title_lower = self.title.lower()
            if not any(keyword.lower() in title_lower for keyword in title_keywords):
                return False
        
        # Check location
        if locations:
            location_lower = self.location.lower()
            if not any(loc.lower() in location_lower for loc in locations):
                return False
        
        # Check work mode
        if work_modes:
            if self.work_mode not in work_modes:
                return False
        
        # Check experience level
        if experience_levels:
            if self.experience_level not in experience_levels:
                return False
        
        # Check minimum salary
        if min_salary is not None and self.salary_min is not None:
            if self.salary_min < min_salary:
                return False
        
        return True
