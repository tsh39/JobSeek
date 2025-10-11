"""
Tests for core models and filtering functionality.
"""

import pytest
from jobseek.models import Job, WorkMode, ExperienceLevel


def test_job_creation():
    """Test creating a job instance."""
    job = Job(
        title="Senior Software Engineer",
        company="Test Corp",
        location="San Francisco, CA",
        url="https://example.com/job/123",
        source="greenhouse",
        work_mode=WorkMode.REMOTE,
        experience_level=ExperienceLevel.SENIOR,
    )
    
    assert job.title == "Senior Software Engineer"
    assert job.company == "Test Corp"
    assert job.work_mode == WorkMode.REMOTE
    assert job.experience_level == ExperienceLevel.SENIOR


def test_job_to_dict():
    """Test converting job to dictionary."""
    job = Job(
        title="Software Engineer",
        company="Test Corp",
        location="Remote",
        url="https://example.com/job/123",
        source="lever",
        salary_min=100000.0,
        salary_max=150000.0,
    )
    
    job_dict = job.to_dict()
    
    assert job_dict["title"] == "Software Engineer"
    assert job_dict["company"] == "Test Corp"
    assert job_dict["salary_min"] == 100000.0
    assert job_dict["salary_max"] == 150000.0
    assert job_dict["source"] == "lever"


def test_job_matches_filters_title():
    """Test filtering by title keywords."""
    job = Job(
        title="Senior Python Engineer",
        company="Test Corp",
        location="Remote",
        url="https://example.com/job/123",
        source="greenhouse",
    )
    
    # Should match
    assert job.matches_filters(title_keywords=["python"])
    assert job.matches_filters(title_keywords=["engineer"])
    assert job.matches_filters(title_keywords=["Senior", "Python"])
    
    # Should not match
    assert not job.matches_filters(title_keywords=["java"])
    assert not job.matches_filters(title_keywords=["javascript", "ruby"])


def test_job_matches_filters_location():
    """Test filtering by location."""
    job = Job(
        title="Software Engineer",
        company="Test Corp",
        location="San Francisco, CA",
        url="https://example.com/job/123",
        source="greenhouse",
    )
    
    # Should match
    assert job.matches_filters(locations=["San Francisco"])
    assert job.matches_filters(locations=["san francisco"])  # case insensitive
    assert job.matches_filters(locations=["CA"])
    
    # Should not match
    assert not job.matches_filters(locations=["New York"])
    assert not job.matches_filters(locations=["Remote"])


def test_job_matches_filters_work_mode():
    """Test filtering by work mode."""
    job = Job(
        title="Software Engineer",
        company="Test Corp",
        location="Remote",
        url="https://example.com/job/123",
        source="greenhouse",
        work_mode=WorkMode.REMOTE,
    )
    
    # Should match
    assert job.matches_filters(work_modes=[WorkMode.REMOTE])
    assert job.matches_filters(work_modes=[WorkMode.REMOTE, WorkMode.HYBRID])
    
    # Should not match
    assert not job.matches_filters(work_modes=[WorkMode.ONSITE])
    assert not job.matches_filters(work_modes=[WorkMode.HYBRID])


def test_job_matches_filters_experience():
    """Test filtering by experience level."""
    job = Job(
        title="Senior Software Engineer",
        company="Test Corp",
        location="Remote",
        url="https://example.com/job/123",
        source="greenhouse",
        experience_level=ExperienceLevel.SENIOR,
    )
    
    # Should match
    assert job.matches_filters(experience_levels=[ExperienceLevel.SENIOR])
    assert job.matches_filters(experience_levels=[ExperienceLevel.SENIOR, ExperienceLevel.LEAD])
    
    # Should not match
    assert not job.matches_filters(experience_levels=[ExperienceLevel.ENTRY])
    assert not job.matches_filters(experience_levels=[ExperienceLevel.MID])


def test_job_matches_filters_salary():
    """Test filtering by minimum salary."""
    job = Job(
        title="Software Engineer",
        company="Test Corp",
        location="Remote",
        url="https://example.com/job/123",
        source="greenhouse",
        salary_min=120000.0,
        salary_max=180000.0,
    )
    
    # Should match
    assert job.matches_filters(min_salary=100000.0)
    assert job.matches_filters(min_salary=120000.0)
    
    # Should not match
    assert not job.matches_filters(min_salary=150000.0)
    assert not job.matches_filters(min_salary=200000.0)


def test_job_matches_filters_combined():
    """Test filtering with multiple criteria."""
    job = Job(
        title="Senior Python Engineer",
        company="Test Corp",
        location="San Francisco, CA (Remote)",
        url="https://example.com/job/123",
        source="greenhouse",
        work_mode=WorkMode.REMOTE,
        experience_level=ExperienceLevel.SENIOR,
        salary_min=150000.0,
    )
    
    # Should match all criteria
    assert job.matches_filters(
        title_keywords=["python"],
        locations=["remote"],
        work_modes=[WorkMode.REMOTE],
        experience_levels=[ExperienceLevel.SENIOR],
        min_salary=140000.0,
    )
    
    # Should fail on one criterion
    assert not job.matches_filters(
        title_keywords=["python"],
        work_modes=[WorkMode.ONSITE],  # Doesn't match
    )


def test_work_mode_enum():
    """Test WorkMode enum."""
    assert WorkMode.REMOTE.value == "remote"
    assert WorkMode.HYBRID.value == "hybrid"
    assert WorkMode.ONSITE.value == "onsite"
    assert WorkMode.UNKNOWN.value == "unknown"


def test_experience_level_enum():
    """Test ExperienceLevel enum."""
    assert ExperienceLevel.INTERNSHIP.value == "internship"
    assert ExperienceLevel.ENTRY.value == "entry"
    assert ExperienceLevel.MID.value == "mid"
    assert ExperienceLevel.SENIOR.value == "senior"
    assert ExperienceLevel.LEAD.value == "lead"
    assert ExperienceLevel.EXECUTIVE.value == "executive"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
