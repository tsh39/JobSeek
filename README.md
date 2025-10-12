# JobSeek

JobSeek is a modular, compliant job scraper designed to aggregate postings from public applicant tracking systems (ATS) such as Greenhouse, Lever, and Workday.  
It demonstrates clean architecture, scalability, and solid software design principles—making it both practical for job discovery and portfolio-ready as a software engineering project.

---

## Purpose
JobSeek helps job seekers surface relevant, high-quality postings efficiently while showcasing best practices in modular design, data ingestion, and filtering.

---

## Development Phases

### 🟩 **Phase 1 — MVP (Current Focus)**
**Goal:** Build a minimal but scalable prototype that fetches jobs from Greenhouse and outputs them to the console and a CSV file.

**Scope:**
- **Source:** Greenhouse only  
- **Filters:** Experience level (Entry, Mid, Senior)  
- **Sorting:** Most recently posted jobs first  
- **Sinks (outputs):** Console and CSV  
- **Architecture:** Core domain + single source + two sinks  
- **CLI Commands:**  
  ```bash
  jobseek fetch --config config.yaml
  jobseek list --since 7d --sort recent
  jobseek export --format csv --out jobs.csv
  ```
- **Testing:**  
  - Unit tests for filters, sort, and CSV writer  
  - Mocked tests for Greenhouse parser  
- **Compliance:** Respect `robots.txt`; no LinkedIn scraping

This phase establishes the foundation—ensuring the pipeline, normalization, and filtering logic work cleanly before expanding.

---

### 🟨 **Phase 2 — Multi-Source & Filtering Expansion**
**Goal:** Introduce more sources and filtering logic while maintaining modularity.

**Planned Additions:**
- **New Sources:** Lever, Workday, and other ATS adapters  
- **Filters:** Location, title keywords, work mode (remote/hybrid/on-site), and salary  
- **Dedupe:** Detect and remove duplicates across ATS sources  
- **Storage:** Add SQLite sink for persistence and future querying  
- **Scheduling:** Implement `watch` mode for recurring scrapes (e.g., every 60 minutes)  
- **Ranking:** Recency + keyword-based relevance scoring

---

### 🟦 **Phase 3 — Advanced Features & Web Interface**
**Goal:** Evolve JobSeek into a more automated and interactive job discovery tool.

**Planned Additions:**
- **Semantic relevance scoring** (e.g., sentence embeddings for matching keywords/skills)  
- **Web API & UI:** FastAPI backend + minimal React or Svelte frontend for browsing, saving, and tagging jobs  
- **Storage:** Transition to Postgres for multi-user or long-term data  
- **Scheduling & Automation:** GitHub Actions or containerized cron for periodic runs  
- **Compliance:** Configurable per-source opt-in and crawl delay enforcement  

---

## Architecture Overview
JobSeek uses a **Hexagonal (Ports & Adapters)** architecture for long-term scalability.

- **Domain Layer:** Core entities and interfaces  
  - `Job` model (normalized schema)  
  - `JobSource` and `JobSink` interfaces  
- **Application Layer:** Orchestrates the pipeline — fetch → normalize → filter → sort → sink  
- **Adapters:**  
  - *Sources* — platform-specific scrapers (Greenhouse, Lever, etc.)  
  - *Sinks* — output modules (Console, CSV, SQLite, Postgres)  
- **Config-Driven:** All behavior controlled by `config.yaml`  
- **Extensible:** Add new sources, filters, or sinks without modifying core logic

---

## Technology Stack
- **Language:** Python 3.12  
- **Core Libraries:** `httpx`, `asyncio`, `pydantic`, `Typer`  
- **Testing:** `pytest`  
- **Linting & Typing:** `ruff`, `mypy`  
- **CI/CD:** GitHub Actions (lint, type-check, tests, coverage badge)  
- **Future:** FastAPI (backend) + React (frontend)

---

## Compliance
- Respects each site’s `robots.txt` and usage terms  
- No automated scraping of LinkedIn or similar protected sources  
- Requests are rate-limited and opt-in per source  
- Legal considerations documented in `LEGAL.md`

---

## Roadmap Summary
| Phase | Focus | Key Deliverables |
|-------|--------|------------------|
| 🟩 **1** | MVP | Greenhouse adapter, experience filter, console & CSV sinks |
| 🟨 **2** | Multi-source expansion | Lever & Workday adapters, more filters, dedupe, SQLite sink |
| 🟦 **3** | Advanced & UI | Semantic ranking, FastAPI + web UI, automation, Postgres |

---

## Project Structure
```
jobseek/
├── domain/
│   └── models.py              # Core data types and interfaces
├── app/
│   ├── config.py              # Configuration parsing and schema
│   └── pipeline.py            # Main orchestration pipeline
├── adapters/
│   ├── sources/
│   │   └── greenhouse.py      # Greenhouse source adapter
│   └── sinks/
│       ├── console.py         # Console output
│       └── csvsink.py         # CSV output
├── cli/
│   └── main.py                # Typer CLI entry point
├── tests/
│   └── test_pipeline.py       # Unit and integration tests
├── README.md
└── LEGAL.md
```

---

## License & Disclaimer
JobSeek is an educational and portfolio project.  
Users are responsible for adhering to all relevant site terms and local regulations when running the scraper.
