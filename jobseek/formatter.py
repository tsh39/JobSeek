"""
Output formatting utilities for job results.
"""

import json
import csv
from typing import List
from pathlib import Path
from jobseek.models import Job


class OutputFormatter:
    """Format job results for output."""
    
    @staticmethod
    def to_json(jobs: List[Job], output_file: str = None) -> str:
        """
        Format jobs as JSON.
        
        Args:
            jobs: List of Job objects
            output_file: Optional file path to write output
            
        Returns:
            JSON string
        """
        job_dicts = [job.to_dict() for job in jobs]
        json_str = json.dumps(job_dicts, indent=2)
        
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(json_str)
        
        return json_str
    
    @staticmethod
    def to_csv(jobs: List[Job], output_file: str = None) -> str:
        """
        Format jobs as CSV.
        
        Args:
            jobs: List of Job objects
            output_file: Optional file path to write output
            
        Returns:
            CSV string
        """
        if not jobs:
            return ""
        
        # Define CSV headers
        headers = [
            'title', 'company', 'location', 'url', 'source',
            'work_mode', 'experience_level', 'salary_min', 'salary_max',
            'salary_currency', 'posted_date', 'linkedin_url', 'keywords'
        ]
        
        # Prepare rows
        rows = []
        for job in jobs:
            job_dict = job.to_dict()
            row = {
                'title': job_dict['title'],
                'company': job_dict['company'],
                'location': job_dict['location'],
                'url': job_dict['url'],
                'source': job_dict['source'],
                'work_mode': job_dict['work_mode'],
                'experience_level': job_dict['experience_level'],
                'salary_min': job_dict.get('salary_min', ''),
                'salary_max': job_dict.get('salary_max', ''),
                'salary_currency': job_dict.get('salary_currency', ''),
                'posted_date': job_dict.get('posted_date', ''),
                'linkedin_url': job_dict.get('linkedin_url', ''),
                'keywords': ','.join(job_dict.get('keywords', [])),
            }
            rows.append(row)
        
        # Write to file or string
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
            return f"CSV written to {output_file}"
        else:
            # Return as string
            import io
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
            return output.getvalue()
    
    @staticmethod
    def to_console(jobs: List[Job], verbose: bool = False) -> str:
        """
        Format jobs for console output.
        
        Args:
            jobs: List of Job objects
            verbose: Include detailed information
            
        Returns:
            Formatted string for console
        """
        if not jobs:
            return "No jobs found."
        
        output = []
        output.append(f"\n{'='*80}")
        output.append(f"Found {len(jobs)} job(s)")
        output.append(f"{'='*80}\n")
        
        for i, job in enumerate(jobs, 1):
            output.append(f"{i}. {job.title}")
            output.append(f"   Company: {job.company}")
            output.append(f"   Location: {job.location}")
            output.append(f"   Work Mode: {job.work_mode.value}")
            output.append(f"   Experience: {job.experience_level.value}")
            
            if job.salary_min and job.salary_max:
                output.append(f"   Salary: ${job.salary_min:,.0f} - ${job.salary_max:,.0f} {job.salary_currency}")
            
            output.append(f"   URL: {job.url}")
            
            if job.linkedin_url:
                output.append(f"   LinkedIn Search: {job.linkedin_url}")
            
            if verbose:
                if job.keywords:
                    output.append(f"   Keywords: {', '.join(job.keywords)}")
                if job.description:
                    desc = job.description[:200] + "..." if len(job.description) > 200 else job.description
                    output.append(f"   Description: {desc}")
            
            output.append(f"   Source: {job.source}")
            output.append("")
        
        return "\n".join(output)
