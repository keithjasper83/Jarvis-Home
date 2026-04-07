# AGENTS.md

## Project Purpose
To build a fully local, self-owned automation and conversational control system. It provides custom web interface and voice interfaces, supports local models, and avoids cloud dependence.

## Source of Truth
- `Master Spec.md` is the primary source of truth.
- `AGENTS.md` acts as the main collaboration contract.
- Any files in `/docs`, `/spec`, `/architecture`, `/infra`, `/packages/*/README*`, `/apps/*/README*`.

## Repository Structure
- `/apps`
- `/packages`
- `/infra`
- `/docs`
- `/scripts`
- `/tests`

## Implementation Principles
- Local-first.
- Deterministic control.
- Separation of concerns.
- Shared capability model.
- Modular packaging.
- Productizability.
- Observability.
- Safe but capable local interrogation.
- Friendly conversational UX.
- No corporate-assistant dependency.

## Workflow Rules
- Agents should follow `Master Spec.md` explicitly.
- Agents should create and update trackers and changelogs when modifying the repo.
- Agents should mark unresolved issues explicitly rather than stopping.
- Agents should read specs and read repo governance before making changes.
- Agents should make meaningful engineering choices when assumptions are needed and document them.

## Copilot and Jules
- Jules implements the changes.
- Copilot reviews, assesses, and requests changes.
- When Copilot requests changes, document rationale in `CHANGELOG-DETAIL.md` and/or `docs/ai/copilot-review-notes.md`.

## File Ownership and Package Boundaries
Respect package boundaries. Do not merge unrelated functionality. Use Docker-compatible service boundaries.
