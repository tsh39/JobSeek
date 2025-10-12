from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Job:
    id: str
    title: str
    company: str
    location: Optional[str]
    description: Optional[str]
    url: str
    release_date: Optional[datetime]
    experience_level: Optional[str]
    salary: Optional[str]


class JobSource:
    async def fetch(self) -> list[Job]:
        """Fetch jobs from source and return a list of Job objects."""
        raise NotImplementedError()


class JobSink:
    async def write(self, jobs: list[Job]) -> None:
        """Write jobs to the sink (console, csv, db, etc.)."""
        raise NotImplementedError()
