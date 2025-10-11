"""
Tests for base scraper functionality.
"""

import pytest
from jobseek.base_scraper import BaseScraper
from jobseek.models import Job, WorkMode, ExperienceLevel


class MockScraper(BaseScraper):
    """Mock scraper for testing."""
    
    def scrape(self):
        return []
    
    def get_source_name(self):
        return "mock"


def test_detect_work_mode_remote():
    """Test detecting remote work mode."""
    scraper = MockScraper()
    
    assert scraper._detect_work_mode("Remote Software Engineer") == WorkMode.REMOTE
    assert scraper._detect_work_mode("Work from home position") == WorkMode.REMOTE
    assert scraper._detect_work_mode("WFH Developer") == WorkMode.REMOTE


def test_detect_work_mode_hybrid():
    """Test detecting hybrid work mode."""
    scraper = MockScraper()
    
    assert scraper._detect_work_mode("Hybrid work model") == WorkMode.HYBRID
    assert scraper._detect_work_mode("Flexible work schedule") == WorkMode.HYBRID
    assert scraper._detect_work_mode("Remote with some hybrid") == WorkMode.HYBRID


def test_detect_work_mode_onsite():
    """Test detecting onsite work mode."""
    scraper = MockScraper()
    
    assert scraper._detect_work_mode("On-site position") == WorkMode.ONSITE
    assert scraper._detect_work_mode("In-office role") == WorkMode.ONSITE
    assert scraper._detect_work_mode("Office based") == WorkMode.ONSITE


def test_detect_work_mode_unknown():
    """Test detecting unknown work mode."""
    scraper = MockScraper()
    
    assert scraper._detect_work_mode("Software Engineer") == WorkMode.UNKNOWN
    assert scraper._detect_work_mode("Developer position") == WorkMode.UNKNOWN


def test_detect_experience_level_internship():
    """Test detecting internship level."""
    scraper = MockScraper()
    
    assert scraper._detect_experience_level("Software Engineering Intern") == ExperienceLevel.INTERNSHIP
    assert scraper._detect_experience_level("Internship - Developer") == ExperienceLevel.INTERNSHIP


def test_detect_experience_level_entry():
    """Test detecting entry level."""
    scraper = MockScraper()
    
    assert scraper._detect_experience_level("Junior Software Engineer") == ExperienceLevel.ENTRY
    assert scraper._detect_experience_level("Entry Level Developer") == ExperienceLevel.ENTRY
    assert scraper._detect_experience_level("Associate Engineer") == ExperienceLevel.ENTRY


def test_detect_experience_level_senior():
    """Test detecting senior level."""
    scraper = MockScraper()
    
    assert scraper._detect_experience_level("Senior Software Engineer") == ExperienceLevel.SENIOR
    assert scraper._detect_experience_level("Sr. Developer") == ExperienceLevel.SENIOR
    assert scraper._detect_experience_level("Staff Engineer") == ExperienceLevel.SENIOR


def test_detect_experience_level_lead():
    """Test detecting lead level."""
    scraper = MockScraper()
    
    assert scraper._detect_experience_level("Lead Engineer") == ExperienceLevel.LEAD
    assert scraper._detect_experience_level("Principal Developer") == ExperienceLevel.LEAD
    assert scraper._detect_experience_level("Architect") == ExperienceLevel.LEAD


def test_detect_experience_level_executive():
    """Test detecting executive level."""
    scraper = MockScraper()
    
    assert scraper._detect_experience_level("Engineering Director") == ExperienceLevel.EXECUTIVE
    assert scraper._detect_experience_level("VP of Engineering") == ExperienceLevel.EXECUTIVE
    assert scraper._detect_experience_level("Chief Technology Officer") == ExperienceLevel.EXECUTIVE


def test_extract_salary():
    """Test salary extraction."""
    scraper = MockScraper()
    
    # Test range format
    min_sal, max_sal, currency = scraper._extract_salary("Salary: $100,000 - $150,000")
    assert min_sal == 100000.0
    assert max_sal == 150000.0
    assert currency == "USD"
    
    # Test k format
    min_sal, max_sal, currency = scraper._extract_salary("Pay: $100k-$150k")
    assert min_sal == 100000.0
    assert max_sal == 150000.0
    
    # Test no salary
    min_sal, max_sal, currency = scraper._extract_salary("Software Engineer position")
    assert min_sal is None
    assert max_sal is None


def test_extract_keywords():
    """Test keyword extraction."""
    scraper = MockScraper()
    
    title = "Senior Python Engineer"
    description = "We are looking for a Python developer with AWS and Docker experience."
    
    keywords = scraper._extract_keywords(title, description)
    
    assert "python" in keywords
    assert "aws" in keywords
    assert "docker" in keywords


def test_generate_linkedin_url():
    """Test LinkedIn URL generation."""
    scraper = MockScraper()
    
    url = scraper._generate_linkedin_url("Test Corp", "Software Engineer")
    
    assert "linkedin.com/jobs/search" in url
    assert "Software%20Engineer" in url
    assert "Test%20Corp" in url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
