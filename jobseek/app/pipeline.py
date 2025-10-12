from __future__ import annotations

import asyncio
from typing import Iterable

from jobseek.domain.models import Job, JobSink, JobSource


async def run_pipeline(
    sources: Iterable[JobSource],
    sinks: Iterable[JobSink],
    limit: int
) -> None:
    """Run the ETL pipeline: fetch from sources (up to a limit), write to sinks."""
    all_jobs: list[Job] = []

    async def fetch_source(src: JobSource):
        return await src.fetch()

    results = await asyncio.gather(*(fetch_source(s) for s in sources))
    for r in results:
        all_jobs.extend(r or [])
        if limit > 0 and len(all_jobs) >= limit:
            all_jobs = all_jobs[:limit]
            break

    # naive sink write
    for sink in sinks:
        await sink.write(all_jobs[:limit] if limit > 0 else all_jobs)
