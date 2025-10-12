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
            writer.writerow(["id", "title", "company", "location", "url", "posted_at", "experience_level"])  # header
            for j in jobs:
                writer.writerow([
                    j.id,
                    j.title,
                    j.company,
                    j.location or "",
                    j.url,
                    j.posted_at.isoformat() if j.posted_at else "",
                    j.experience_level or "",
                ])
