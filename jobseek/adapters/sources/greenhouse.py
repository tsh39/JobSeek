from __future__ import annotations

from typing import List
from jobseek.domain.models import Job, JobSource


class GreenhouseSource(JobSource):
    async def fetch(self) -> List[Job]:
        # TODO: call Greenhouse endpoints
        return []
