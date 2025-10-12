from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Optional

import typer # CLI GUI
from jobseek.app.config import load_config # Load config of sources and sinks
from jobseek.app.pipeline import run_pipeline
from jobseek.adapters.sinks.console import ConsoleSink
from jobseek.adapters.sinks.csvsink import CSVSink
from jobseek.adapters.sources.greenhouse import GreenhouseSource


app = typer.Typer(help="JobSeek CLI")


@app.command()
def fetch(config: Optional[Path] = typer.Option(None, help="Path to config.yaml")):
    """Fetch jobs and write to configured sinks (console, csv)."""
    cfg = load_config(config) if config else None
    # minimal demo: run greenhouse -> console
    sources = [GreenhouseSource()]
    sinks = [ConsoleSink(), CSVSink("jobs.csv")]
    asyncio.run(run_pipeline(sources, sinks))


if __name__ == "__main__":
    app()
