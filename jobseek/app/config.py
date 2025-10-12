"""Configuration parsing utilities for JobSeek."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError


class FilterSettings(BaseModel):
    """User-defined filtering preferences loaded from config.yaml."""

    experience_levels: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    salary_min: int | None = None
    salary_max: int | None = None
    work_modes: list[str] = Field(default_factory=list)
    title_keywords: list[str] = Field(default_factory=list)


class AppConfig(BaseModel):
    """Top-level configuration schema."""

    filters: FilterSettings = Field(default_factory=FilterSettings)
    sources: dict[str, dict[str, Any]] = Field(default_factory=dict)
    sinks: dict[str, dict[str, Any]] = Field(default_factory=dict)


def load_config(path: Path) -> AppConfig:
    """Load and validate configuration from a YAML file."""

    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    try:
        return AppConfig.model_validate(data)
    except ValidationError as exc:
        raise RuntimeError(f"Invalid config file at {path}") from exc
