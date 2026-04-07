# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initialized core database architecture utilizing SQLAlchemy 2.0.
- Scaffolded Alembic migrations environment.
- Added initial data models matching Section 27 (`devices`, `capabilities`, `command_executions`, `conversation_turns`).
- Created missing directory structures and package definitions in `apps/` and `packages/` as described by Section 7.
- Initialized configuration management system in `packages/configuration/settings.py` (Section 30).
- Standardized logging system producing structured JSON in `packages/logging_audit/logger.py` (Section 31).
- Set up project `requirements.txt` listing primary web stack components.

- Initial project scaffolding and root governance files (`AGENTS.md`, `README.md`, `CHANGELOG.md`, `CHANGELOG-DETAIL.md`, `CONTRIBUTING.md`, `REPOSITORY-STRUCTURE.md`, `ROADMAP.md`, `DECISIONS.md`, `KNOWN-ISSUES.md`).
- `docs/section-tracker.md` to track progress of the 42 sections from `Master Spec.md`.
- Scaffolded core repository structure (`apps`, `packages`, `infra`, `docs`, `scripts`, `tests`).
- Created initial empty technical documentation and AI collaboration rules.
- Set up placeholder files for `apps/api` and core domain packages.
### Fixed
- Moved `parse_spec.py` and `generate_section_tracker.py` into `scripts/` directory to match documented repo structure.
- Added explicit `encoding="utf-8"` to all file I/O in both scripts; added `ensure_ascii=False` to JSON output and `newline="\n"` to markdown output for cross-platform stability.
- Updated internal path references in both scripts using `pathlib.Path(__file__).parent.parent` (repo root).
- Removed unused `Optional` import from `infra/db/schema.py`; clarified it is a stub not yet a runtime ORM model.
- Added `parsed_sections.json` to `.gitignore` as a generated artifact; removed it from version control.

