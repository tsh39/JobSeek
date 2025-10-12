from __future__ import annotations

import asyncio
from jobseek.app.pipeline import run_pipeline
from jobseek.adapters.sinks.console import ConsoleSink
from jobseek.adapters.sources.greenhouse import GreenhouseSource


def test_pipeline_runs_without_error():
    # Basic smoke test ensuring pipeline orchestration works with stubs
    asyncio.run(run_pipeline([GreenhouseSource()], [ConsoleSink()], limit=5))
