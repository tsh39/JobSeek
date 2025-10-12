"""Typer CLI entry point for JobSeek."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from jobseek.app.config import load_config

app = typer.Typer(help="JobSeek CLI for fetching and exporting job postings.")


@app.command()
def fetch(config: Annotated[Path, typer.Option(help="Path to config.yaml")]) -> None:
    """Fetch jobs according to the provided configuration."""

    load_config(config)
    typer.echo("Fetch command not implemented yet.")


def run() -> None:
    """Entrypoint used by scripts."""

    app()


if __name__ == "__main__":
    run()
