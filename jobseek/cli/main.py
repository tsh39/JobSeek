import asyncio
import typer
from pathlib import Path
from jobseek.app.config import load_config, Config
from jobseek.app.pipeline import run_pipeline
from jobseek.adapters.sources.greenhouse import GreenhouseSource
from jobseek.adapters.sinks.console import ConsoleSink
from jobseek.adapters.sinks.csvsink import CSVSink

app = typer.Typer()

@app.command()
def fetch(
    config: Path = typer.Option(None, help="Path to config.yaml"),
    # board: str = typer.Option(None, help="Greenhouse board token"),
    csv: Path = typer.Option("jobs.csv", help="CSV output path"),
    console: bool = typer.Option(True, help="Also print to console"),
    # only_us: bool = typer.Option(False, help="Filter to US jobs"),
    limit: int = typer.Option(0, help="Fetch at most N jobs (0 = all)"),
):
    cfg = load_config(config) if config else Config() # TODO: use cfg in sources/sinks
    # board = board or cfg.get("greenhouse", {}).get("board")
    sources = [GreenhouseSource()]
    sinks = [CSVSink(str(csv))] + ([ConsoleSink()] if console else [])

    # You can pass flags via cfg to the pipeline, or preprocess in sources/sinks
    asyncio.run(run_pipeline(sources, sinks, limit=limit))

if __name__ == "__main__":
    app()