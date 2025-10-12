"""Tests for the JobSeek pipeline orchestration."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Iterable, Sequence

import pytest

from jobseek.app.pipeline import run_pipeline
from jobseek.domain.models import Job, JobSink, JobSource


class DummySource(JobSource):
    def __init__(self, jobs: Sequence[Job]) -> None:
        self._jobs = jobs

    async def fetch(self) -> Iterable[Job]:
        return list(self._jobs)


class DummySink(JobSink):
    def __init__(self) -> None:
        self.received: list[Job] = []

    async def write(self, jobs: Iterable[Job]) -> None:
        self.received.extend(jobs)


@pytest.mark.asyncio
async def test_pipeline_deduplicates_jobs() -> None:
    job = Job(
        id="1",
        title="Software Engineer",
        company="Example",
        location="Remote",
        created_at=datetime.utcnow(),
        apply_url="https://example.com/jobs/1",
    )

    source_one = DummySource([job])
    source_two = DummySource([job])
    sink = DummySink()

    await run_pipeline([source_one, source_two], [sink])

    assert len(sink.received) == 1
