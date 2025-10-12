"""Console sink adapter."""

from __future__ import annotations

from typing import Iterable

from jobseek.domain.models import Job, JobSink


class ConsoleSink(JobSink):
    """Print jobs to stdout."""

    async def write(self, jobs: Iterable[Job]) -> None:
        for job in jobs:
            print(f"{job.company} — {job.title} ({job.location}) :: {job.apply_url}")
