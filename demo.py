"""
Demo script showing JobSeek functionality without network requests.

This script creates mock job data to demonstrate the filtering
and output formatting capabilities.
"""

from jobseek.models import Job, WorkMode, ExperienceLevel
from jobseek.formatter import OutputFormatter


def create_mock_jobs():
    """Create sample job data for demonstration."""
    jobs = [
        Job(
            title="Senior Software Engineer",
            company="Tech Corp",
            location="San Francisco, CA (Remote)",
            url="https://boards.greenhouse.io/techcorp/jobs/123",
            source="greenhouse",
            description="Looking for a senior engineer with Python and AWS experience.",
            work_mode=WorkMode.REMOTE,
            experience_level=ExperienceLevel.SENIOR,
            salary_min=150000.0,
            salary_max=200000.0,
            linkedin_url="https://www.linkedin.com/jobs/search/?keywords=Senior%20Software%20Engineer%20Tech%20Corp",
            keywords=["python", "aws", "docker", "kubernetes"],
        ),
        Job(
            title="Junior Frontend Developer",
            company="Startup Inc",
            location="New York, NY",
            url="https://jobs.lever.co/startup/jobs/456",
            source="lever",
            description="Entry-level position for a React developer.",
            work_mode=WorkMode.HYBRID,
            experience_level=ExperienceLevel.ENTRY,
            salary_min=80000.0,
            salary_max=100000.0,
            linkedin_url="https://www.linkedin.com/jobs/search/?keywords=Junior%20Frontend%20Developer%20Startup%20Inc",
            keywords=["react", "javascript", "frontend"],
        ),
        Job(
            title="Lead Backend Engineer",
            company="Enterprise LLC",
            location="Seattle, WA",
            url="https://enterprise.wd1.myworkdayjobs.com/careers/789",
            source="workday",
            description="Lead a team of backend engineers working on microservices.",
            work_mode=WorkMode.ONSITE,
            experience_level=ExperienceLevel.LEAD,
            salary_min=180000.0,
            salary_max=250000.0,
            linkedin_url="https://www.linkedin.com/jobs/search/?keywords=Lead%20Backend%20Engineer%20Enterprise%20LLC",
            keywords=["java", "spring", "microservices", "kubernetes"],
        ),
        Job(
            title="Machine Learning Engineer",
            company="AI Innovations",
            location="Remote",
            url="https://boards.greenhouse.io/aiinnovations/jobs/321",
            source="greenhouse",
            description="Work on cutting-edge ML models for computer vision.",
            work_mode=WorkMode.REMOTE,
            experience_level=ExperienceLevel.MID,
            salary_min=130000.0,
            salary_max=170000.0,
            linkedin_url="https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning%20Engineer%20AI%20Innovations",
            keywords=["python", "machine learning", "tensorflow", "pytorch"],
        ),
        Job(
            title="Engineering Intern",
            company="Big Tech Co",
            location="Austin, TX",
            url="https://jobs.lever.co/bigtech/jobs/654",
            source="lever",
            description="Summer internship for computer science students.",
            work_mode=WorkMode.HYBRID,
            experience_level=ExperienceLevel.INTERNSHIP,
            linkedin_url="https://www.linkedin.com/jobs/search/?keywords=Engineering%20Intern%20Big%20Tech%20Co",
            keywords=["python", "java", "internship"],
        ),
    ]
    return jobs


def demo_filtering():
    """Demonstrate filtering capabilities."""
    print("\n" + "="*80)
    print("JobSeek Demo - Filtering and Output")
    print("="*80 + "\n")
    
    jobs = create_mock_jobs()
    formatter = OutputFormatter()
    
    # Show all jobs
    print("\n--- ALL JOBS ---")
    print(formatter.to_console(jobs))
    
    # Filter by remote work mode
    print("\n--- REMOTE JOBS ONLY ---")
    remote_jobs = [j for j in jobs if j.matches_filters(work_modes=[WorkMode.REMOTE])]
    print(formatter.to_console(remote_jobs))
    
    # Filter by experience level
    print("\n--- SENIOR/LEAD POSITIONS ---")
    senior_jobs = [j for j in jobs if j.matches_filters(
        experience_levels=[ExperienceLevel.SENIOR, ExperienceLevel.LEAD]
    )]
    print(formatter.to_console(senior_jobs))
    
    # Filter by keywords
    print("\n--- PYTHON JOBS ---")
    python_jobs = [j for j in jobs if j.matches_filters(title_keywords=["python", "machine learning"])]
    print(formatter.to_console(python_jobs))
    
    # Filter by minimum salary
    print("\n--- JOBS WITH SALARY >= $150K ---")
    high_salary_jobs = [j for j in jobs if j.matches_filters(min_salary=150000)]
    print(formatter.to_console(high_salary_jobs))
    
    # Multiple filters combined
    print("\n--- REMOTE + SENIOR + PYTHON ---")
    filtered = [j for j in jobs if j.matches_filters(
        title_keywords=["engineer"],
        work_modes=[WorkMode.REMOTE],
        experience_levels=[ExperienceLevel.SENIOR, ExperienceLevel.MID],
    )]
    print(formatter.to_console(filtered, verbose=True))


def demo_output_formats():
    """Demonstrate different output formats."""
    print("\n" + "="*80)
    print("Output Format Demo")
    print("="*80 + "\n")
    
    jobs = create_mock_jobs()
    formatter = OutputFormatter()
    
    # JSON output
    print("\n--- JSON FORMAT (first 2 jobs) ---")
    json_output = formatter.to_json(jobs[:2])
    print(json_output[:500] + "...\n")
    
    # CSV output
    print("\n--- CSV FORMAT ---")
    csv_output = formatter.to_csv(jobs[:3])
    print(csv_output)
    
    # Export to files
    print("\n--- EXPORTING TO FILES ---")
    formatter.to_json(jobs, "demo_jobs.json")
    print("✓ Exported to demo_jobs.json")
    
    formatter.to_csv(jobs, "demo_jobs.csv")
    print("✓ Exported to demo_jobs.csv")


def demo_job_statistics():
    """Show job statistics."""
    print("\n" + "="*80)
    print("Job Statistics")
    print("="*80 + "\n")
    
    jobs = create_mock_jobs()
    
    # Count by work mode
    work_mode_counts = {}
    for job in jobs:
        mode = job.work_mode.value
        work_mode_counts[mode] = work_mode_counts.get(mode, 0) + 1
    
    print("Jobs by Work Mode:")
    for mode, count in work_mode_counts.items():
        print(f"  {mode.capitalize()}: {count}")
    
    # Count by experience level
    exp_counts = {}
    for job in jobs:
        level = job.experience_level.value
        exp_counts[level] = exp_counts.get(level, 0) + 1
    
    print("\nJobs by Experience Level:")
    for level, count in exp_counts.items():
        print(f"  {level.capitalize()}: {count}")
    
    # Count by ATS source
    source_counts = {}
    for job in jobs:
        source = job.source
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print("\nJobs by ATS Platform:")
    for source, count in source_counts.items():
        print(f"  {source.capitalize()}: {count}")
    
    # Salary statistics
    salaries = [j.salary_min for j in jobs if j.salary_min]
    if salaries:
        print(f"\nSalary Range:")
        print(f"  Min: ${min(salaries):,.0f}")
        print(f"  Max: ${max(salaries):,.0f}")
        print(f"  Avg: ${sum(salaries)/len(salaries):,.0f}")


if __name__ == "__main__":
    demo_filtering()
    demo_output_formats()
    demo_job_statistics()
    
    print("\n" + "="*80)
    print("Demo Complete!")
    print("="*80)
    print("\nTo use with real data, try:")
    print("  jobseek greenhouse --company stripe")
    print("  jobseek lever --company netflix --keywords python --work-mode remote")
    print("\nSee README.md for more examples and documentation.")
    print("="*80 + "\n")
