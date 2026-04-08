# KNOWN ISSUES

This file tracks open issues discovered during review passes. Issues are grouped by domain and should be resolved before the relevant spec section is marked complete.

---

## Review Pass: 2026-04-07 — Comprehensive Scaffolding Review
**Reviewer:** Copilot Review Agent  
**Scope:** All 42 Master Spec sections vs. actual repository state  
**Status:** 3/42 spec sections started; 0/42 fully complete

---

## [INFRA-001] docker-compose.yml is empty — no services defined

**File:** `infra/docker/docker-compose.yml`  
**Spec:** Section 1 (item 1), Section 34  
**Severity:** Critical  

`docker-compose.yml` exists but is completely empty. No Dockerfiles exist for any service. The platform cannot be started or tested in its intended Docker environment.

**Required:**
- Define services for `api`, `worker`, `voice-gateway` (minimum)
- Create `Dockerfile` per service under `apps/`
- Add `.env.template` for environment variable documentation
- Document host-networking requirements for LAN discovery
- Add volume mounts for logs, database, configuration

---

## [INFRA-002] No Dockerfiles for any deployable service

**File:** `apps/api/`, `apps/worker/`, `apps/voice_gateway/`, `apps/devtools/`  
**Spec:** Section 34  
**Severity:** Critical  

None of the four app directories contain a `Dockerfile`. Services cannot be containerized or independently deployed.

---

## [DB-001] infra/db/schema.py is a stub — no real ORM models

**File:** `infra/db/schema.py`  
**Spec:** Section 26, Section 27  
**Severity:** High  

The schema file contains only placeholder Python classes with no SQLAlchemy/SQLModel decorators. No tables can be created or queried. Full entity definitions required per Section 27 (devices, capabilities, discovery jobs, interrogation reports, conversations, voice turns, audit events, model registry, config, etc.).

---

## [DB-002] No Alembic migration setup

**File:** `infra/db/` (missing `alembic.ini`, `alembic/` directory)  
**Spec:** Section 26, Section 8  
**Severity:** High  

`alembic` is listed in `requirements.txt` but no migration environment has been initialized. No migrations exist. Without this, schema versioning and upgrades are impossible.

---

## [DB-003] docs/database/schema.md is empty

**File:** `docs/database/schema.md`  
**Spec:** Section 35  
**Severity:** Medium  

The database schema documentation file exists but contains no content. Schema entity descriptions, field definitions, and relationship diagrams are required.

---

## [API-001] API routes limited to placeholder root and health endpoints

**File:** `apps/api/routes.py`  
**Spec:** Section 10, Section 28  
**Severity:** High  

Only `GET /` and `GET /health` are defined. All 17 page routes from Section 10 are missing, including: `/devices`, `/discovery`, `/interrogation/*`, `/commands`, `/voice`, `/models`, `/audio`, `/logs`, `/audit`, `/config`, `/ui`, `/extensions`, `/health`, `/about`.

---

## [API-002] templates.py uses a raw HTML string instead of Jinja2

**File:** `apps/api/templates.py`  
**Spec:** Section 8, Section 11  
**Severity:** High  

The current template system is a plain Python string with no Jinja2, no Tailwind, no HTMX, no Alpine.js, and no template inheritance. This violates the UI requirements in Sections 8 and 11. Jinja2 template files must be created under a `templates/` directory and loaded via FastAPI's `Jinja2Templates`.

---

## [UI-001] No Jinja2 template files (.html) exist anywhere

**Spec:** Section 9, Section 10, Section 11  
**Severity:** High  

There are no `.html` template files in the repository. None of the 17 required pages from Section 10 have been templated. A `templates/` directory must be created with base layouts and page templates.

---

## [UI-002] No Tailwind CSS integration

**Spec:** Section 8, Section 11  
**Severity:** High  

Tailwind CSS is required per Section 8 and 11. No `tailwind.config.js`, no CDN link in any template, no CSS build setup. All UI is unstyled.

---

## [UI-003] ui_shell, ui_components, ui_customization packages are empty stubs

**Files:** `packages/ui_shell/`, `packages/ui_components/`, `packages/ui_customization/`  
**Spec:** Section 11  
**Severity:** High  

All three UI packages contain only `__init__.py`. No layout macros, base templates, component library, theme tokens, or override-layer logic have been implemented.

---

## [CORE-001] Shared capability model not implemented

**File:** `packages/capability_engine/`  
**Spec:** Section 17 — SHARED CAPABILITY MODEL  
**Severity:** Critical  

The capability engine package contains only `__init__.py`. The capability model is described as "the heart of the system" in the spec. No capability definitions, schemas, parameter contracts, execution contracts, safety levels, or capability registry exist.

---

## [CORE-002] Device registry not implemented

**File:** `packages/device_registry/`  
**Spec:** Section 19  
**Severity:** Critical  

The device registry package contains only `__init__.py`. No device model, registration logic, persistence mapping, capability binding, inventory query, or state snapshot logic has been implemented.

---

## [CORE-003] Device adapter abstraction not implemented

**Files:** `packages/device_adapters_base/`, `packages/device_adapters_http/`, `packages/device_adapters_ssh/`, `packages/device_adapters_mqtt/`, `packages/device_adapters_custom/`  
**Spec:** Section 20  
**Severity:** Critical  

All five adapter packages are empty stubs. No base adapter interface (`probe()`, `get_capabilities()`, `execute_command()`, `get_status()`, `interrogate()`, `validate_config()`, `test_connection()`), no HTTP/SSH/MQTT/Tapo adapter implementations.

---

## [CORE-004] Discovery subsystem not implemented

**File:** `packages/discovery/`  
**Spec:** Section 21  
**Severity:** High  

The discovery package contains only `__init__.py`. No subnet scanning, host reachability testing, port probing, fingerprinting, or job tracking logic exists.

---

## [CORE-005] Interrogation subsystem not implemented

**File:** `packages/interrogation/`  
**Spec:** Section 22  
**Severity:** High  

The interrogation package contains only `__init__.py`. No safe probe workflows, SSH/Telnet/HTTP interrogation logic, structured findings, or report generation exist.

---

## [CORE-006] Conversation/session package not implemented

**File:** `packages/conversation/`  
**Spec:** Section 14  
**Severity:** High  

The conversation package contains only `__init__.py`. No session models, turn lifecycle, clarification handling, context scopes, or conversational state management exist.

---

## [CORE-007] core_domain entities not defined

**File:** `packages/core_domain/`  
**Spec:** Section 6  
**Severity:** High  

The core domain package contains only `__init__.py`. No shared domain entities, value objects, enums, IDs, or lifecycle concepts are defined. This blocks all downstream packages that depend on the domain model.

---

## [VOICE-001] Voice gateway app is an empty stub

**File:** `apps/voice_gateway/`  
**Spec:** Section 12, Section 13  
**Severity:** High  

`apps/voice_gateway/` contains only `__init__.py`. The voice pipeline (audio capture → STT → transcript → conversation manager → capability planner → command execution → TTS → audio output) has not been started.

---

## [VOICE-002] Voice orchestration package not implemented

**File:** `packages/voice_orchestration/`  
**Spec:** Section 12, Section 13  
**Severity:** High  

Contains only `__init__.py`. No wake-word/activation strategy, session gating, STT dispatching, intent resolution hooks, or TTS coordination logic exist.

---

## [VOICE-003] STT packages are empty stubs

**Files:** `packages/stt_base/`, `packages/stt_whisper/`  
**Spec:** Section 16  
**Severity:** High  

Both STT packages contain only `__init__.py`. No STT provider abstraction interface or Whisper integration exists.

---

## [VOICE-004] TTS packages are empty stubs

**Files:** `packages/tts_base/`, `packages/tts_piper/`  
**Spec:** Section 16  
**Severity:** High  

Both TTS packages contain only `__init__.py`. No TTS provider abstraction interface or Piper integration exists.

---

## [VOICE-005] LLM packages are empty stubs

**Files:** `packages/llm_base/`, `packages/llm_lmstudio/`, `packages/model_registry/`  
**Spec:** Section 15  
**Severity:** High  

All three LLM-related packages contain only `__init__.py`. No LLM provider abstraction, LM Studio integration, model profiles, model discovery, routing policy, or model registry exist.

---

## [WORKER-001] Background worker service not implemented

**File:** `apps/worker/`  
**Spec:** Section 33  
**Severity:** High  

`apps/worker/` contains only `__init__.py`. No background job infrastructure, discovery polling, interrogation scheduling, maintenance tasks, retry logic, or queue integration has been set up.

---

## [AUTHN-001] Authentication/authorization package is an empty stub

**File:** `packages/authn_authz/`  
**Spec:** Section 29  
**Severity:** Medium  

Contains only `__init__.py`. No auth boundary, even a stub interface, has been defined. Section 29 requires this boundary be established early even if initial auth is simple.

---

## [TEST-001] No integration tests exist

**File:** `tests/integration/`  
**Spec:** Section 36  
**Severity:** Medium  

`tests/integration/` contains only `__init__.py`. No integration tests cover any API routes, database operations, adapter interactions, or service boundaries.

---

## [TEST-002] No end-to-end tests exist

**File:** `tests/e2e/`  
**Spec:** Section 36  
**Severity:** Medium  

`tests/e2e/` contains only `__init__.py`. No E2E test scenarios exist for any user-facing workflow.

---

## [TEST-003] No test fixtures defined

**File:** `tests/fixtures/`  
**Spec:** Section 36  
**Severity:** Medium  

`tests/fixtures/` contains only `__init__.py`. No shared test fixtures, mock devices, sample capability definitions, or seed data are available for tests.

---

## [DEP-001] requirements.txt has no version pinning

**File:** `requirements.txt`  
**Spec:** Section 8  
**Severity:** Medium  

All five dependencies (`fastapi`, `sqlalchemy`, `pydantic`, `alembic`, `jinja2`) are listed without version constraints. This will cause non-reproducible builds and potential future breakage. Missing: `uvicorn`, `python-dotenv`, `httpx` (for testing), `pytest`, `pytest-asyncio`.

---

## [DOC-001] Multiple required documentation files are empty

**Files:**  
- `docs/architecture-overview.md`  
- `docs/implementation-plan.md`  
- `docs/progress-log.md`  
- `docs/database/schema.md`  
- `docs/ai/copilot-review-notes.md`  
- `KNOWN-ISSUES.md` (was empty before this review)  

**Spec:** Section 35  
**Severity:** Medium  

Six documentation files were scaffolded but left empty. They must be populated as work proceeds.

---

## [TRACKER-001] 39 of 42 spec sections remain "Unstarted"

**File:** `docs/section-tracker.md`  
**Spec:** All sections  
**Severity:** Informational  

Only 3 sections are in "Started" state (7, 30, 31). 39 sections remain completely unaddressed. This is the top-level summary of the implementation debt.

**Priority order for next implementation passes:**
1. Section 26/27 — Database (entities, migrations)
2. Section 6 — Core domain model
3. Section 17 — Shared capability model
4. Section 19 — Device registry
5. Section 20 — Device adapter abstraction
6. Section 10 + Section 9/11 — Page map + UI shell
7. Section 28 — API design and routes
8. Section 34 — Docker/deployment
9. Section 12/13/16 — Voice pipeline
10. Section 15 — LLM/model registry
