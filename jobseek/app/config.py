from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class Config(BaseModel):
    sources: dict[str, Any] = {}
    sinks: dict[str, Any] = {}
    filters: dict[str, Any] = {}


def load_config(path: str | Path) -> Config:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Config.parse_obj(data or {})
