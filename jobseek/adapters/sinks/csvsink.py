"""CSV sink adapter."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from jobseek.domain.models import Job, JobSink


class CsvSink(JobSink):
    """Write jobs to a CSV file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    async def write(self, jobs: Iterable[Job]) -> None:
        with self.path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                [
                    "id",
                    "title",
                    "company",
                    "location",
                    "created_at",
                    "apply_url",
                    "remote",
                    "salary",
                    "description",
                ]
            )
            for job in jobs:
                writer.writerow(
                    [
                        job.id,
                        job.title,
                        job.company,
                        job.location,
                        job.created_at.isoformat(),
                        job.apply_url,
                        job.remote,
                        job.salary or "",
                        job.description or "",
                    ]
                )
