from __future__ import annotations

from typing import Iterable
from jobseek.domain.models import Job, JobSink


class ConsoleSink(JobSink):
    async def write(self, jobs: Iterable[Job]) -> None:
        for j in jobs:
            print(f"{j.posted_at or 'UNKNOWN'}\t{j.company}\t{j.title}\t{j.url}")
