"""Domain models and abstract interfaces for JobSeek."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Protocol


@dataclass(slots=True)
class Job:
    """Represents a normalized job posting."""

    id: str
    title: str
    company: str
    location: str
    created_at: datetime
    apply_url: str
    remote: bool = False
    salary: str | None = None
    description: str | None = None


class JobSource(Protocol):
    """Adapter interface for fetching raw jobs from an external system."""

    async def fetch(self) -> Iterable[Job]:
        """Collect jobs from the underlying source."""
        raise NotImplementedError


class JobSink(Protocol):
    """Adapter interface for persisting or displaying jobs."""

    async def write(self, jobs: Iterable[Job]) -> None:
        """Persist or emit the provided jobs."""
        raise NotImplementedError
