"""Application pipeline orchestrating job ingestion and output."""

from __future__ import annotations

from typing import Iterable, Sequence

from jobseek.domain.models import Job, JobSink, JobSource


async def run_pipeline(
    sources: Sequence[JobSource],
    sinks: Sequence[JobSink],
) -> None:
    """Fetch jobs from sources, dedupe, and send to sinks."""

    jobs = []
    seen_ids: set[str] = set()

    for source in sources:
        async for job in _yield_jobs(source):
            if job.id in seen_ids:
                continue
            seen_ids.add(job.id)
            jobs.append(job)

    for sink in sinks:
        await sink.write(jobs)


async def _yield_jobs(source: JobSource) -> Iterable[Job]:
    """Yield jobs from a source, normalizing sync/async iterables."""

    result = await source.fetch()
    for job in result:
        yield job
