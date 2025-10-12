from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable
from jobseek.domain.models import Job, JobSink


class CSVSink(JobSink):
    def __init__(self, out: str | Path):
        self.out = Path(out)

    async def write(self, jobs: Iterable[Job]) -> None:
        with self.out.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "company", "location", "description", 
                             "url", "release_date", "experience_level", "salary"])  # header
            for job in jobs:
                writer.writerow([
                    job.id,
                    job.title,
                    job.company,
                    job.location or "",
                    job.description or "",
                    job.url,
                    job.release_date.isoformat() if job.release_date else "",
                    job.experience_level or "",
                    job.salary or "",
                ])
