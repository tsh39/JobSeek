"""Greenhouse ATS source adapter."""

from __future__ import annotations

from typing import Iterable

from jobseek.domain.models import Job, JobSource


class GreenhouseSource(JobSource):
    """Fetch jobs from the Greenhouse API."""

    def __init__(self, board_token: str) -> None:
        self.board_token = board_token

    async def fetch(self) -> Iterable[Job]:
        """Fetch jobs for the configured board token."""

        # TODO: Implement HTTP fetching via httpx.
        return []
