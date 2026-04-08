# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Created the Dark Mode UI and expanded layout templates (`dashboard.html`, `devices.html`).
- Setup FastAPI and Jinja2 routing foundation for the primary Web Interface (`apps/api/routes.py`).
- Added foundational Tailwind+Jinja2 templates for the dashboard per Sections 9-11.
- Created the `SshLocalAdapter` integrating Paramiko for secure shell interrogation and command execution.
- Built the `HttpLocalAdapter` translating capability IDs into RESTful network requests (Section 20 & 24).
- Wired the `CommandExecutionEngine` directly to the `DeviceRegistry` and `AdapterRegistry` for dynamic end-to-end execution.
- Initialized core database architecture utilizing SQLAlchemy 2.0.
- Scaffolded Alembic migrations environment.
- Added initial data models matching Section 27 (`devices`, `capabilities`, `command_executions`, `conversation_turns`).
- Implemented core Capability Engine (`CapabilityDefinition`, `SafetyLevel`, `ExecutionContract`, `CapabilityRegistry`).
- Implemented `CommandExecutionEngine` with request parameter validation and execution lifecycle tracking.
- Implemented `DeviceRegistry` for managing persistent device inventory mapping to DB operations.
- Established the `BaseAdapter` abstract class defining the standard protocol for interacting with external hardware.
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

