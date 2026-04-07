You are acting as a principal systems architect, principal Python engineer, principal voice systems engineer, principal UI engineer, principal platform engineer, and principal automation designer.

You are to design and scaffold a serious, production-minded, fully local conversational automation platform that replaces cloud assistants such as Alexa and Siri with a custom, self-owned system. This is not a toy assistant, not a generic chatbot wrapper, not a smart-home hobby dashboard, and not a thin integration layer over existing corporate ecosystems. It is a local-first control platform, built to run on self-owned hardware, with deterministic device control, a web interface, a voice interface, strong observability, modular packaging, and future productization in mind.

This brief is intentionally thorough. Do not stop every few minutes to ask obvious questions that can be answered through reasonable engineering assumptions. Make sensible, explicit decisions, document them, and proceed. When assumptions are needed, state them and continue. The objective is to get meaningful architecture, scaffolding, package structure, interface definitions, and implementation started immediately.

The resulting platform should feel like a real conversational automation system: friendly, capable, responsive, inspectable, and under full local control. Think “Jarvis, but real, practical, and engineerable,” not film magic and not corporate hand-waving.

---

## SECTION 1 — PRIMARY GOAL

Build a fully local, self-owned automation and conversational control system that:

1. Runs primarily in Docker on a Windows host.
2. Uses Python as the primary implementation language.
3. Provides a custom web interface for configuration, inspection, control, observability, and administration.
4. Provides a voice interface for natural conversational control.
5. Uses the same underlying capability model for both web and voice so that both interfaces expose the same actions, statuses, and workflows.
6. Supports direct local interaction with devices over local protocols such as HTTP, SSH, Telnet where explicitly enabled, MQTT, sockets, and custom adapters.
7. Avoids cloud dependence wherever practical.
8. Treats cloud APIs as last resort, not preferred path.
9. Can interrogate local devices to determine whether they are locally controllable, even when vendors officially push cloud usage.
10. Supports local language models hosted on the same environment, with model discovery, selection, configuration, and runtime observability.
11. Speaks responses back through the platform’s TTS layer, with the LLM generating text only.
12. Maintains strict separation of concerns so faults can be isolated quickly.
13. Is modular enough that subsystems, packages, and UI modules can later be independently released, versioned, documented, or customized.
14. Is suitable for eventual distribution to multiple users or deployments, with per-user, per-deployment, or per-serial-number customization capability.

---

## SECTION 2 — HOST ENVIRONMENT AND OPERATING ASSUMPTIONS

Assume the main host environment is a Windows machine that:

1. Runs Docker / Docker Desktop.
2. Acts as the primary host for the automation platform.
3. Also acts as the local model host.
4. Has an NVIDIA GPU including at least a 4070 Ti available.
5. Runs LM Studio for model hosting and local inference access.
6. May host more than one model at a time or allow switching between models.
7. Has local storage available for logs, configuration, model mappings, reports, and persistent databases.
8. Has one or more USB audio devices attached, including a USB Yeti microphone for input.
9. May have one or more speakers / local audio output devices for voice response.
10. Is part of a LAN containing consumer devices, ESP-based devices, local endpoints, and potentially poorly documented smart-home devices.

Assume Dockerized services may need access to:

* LAN discovery functions
* outbound local network access
* audio pipeline services
* LM Studio endpoints
* databases
* log storage
* persistent configuration
* possibly host networking in selected cases where justified

Assume Windows-specific operational considerations matter, and design with them in mind.

---

## SECTION 3 — NON-NEGOTIABLE DESIGN PRINCIPLES

The system must follow these principles:

1. Local-first.
   All core functions should work locally wherever technically possible.

2. Deterministic control.
   Commands such as volume control, device toggling, thermostat changes, music volume changes, and light scenes should resolve to local, inspectable actions, not opaque cloud workflows.

3. Separation of concerns.
   Voice, STT, TTS, model routing, command parsing, capability resolution, device registry, device execution, discovery, interrogation, UI rendering, logging, and persistence must be architecturally distinct.

4. Shared capability model.
   Voice and web must not have separate capability logic. A capability defined once must surface through both.

5. Modular packaging.
   Organize the codebase into independent packages/modules where practical, with explicit APIs and documentation boundaries.

6. Productizability.
   The architecture should allow future packaging, internal distribution, third-party release, and deployment customization.

7. Observability.
   Every significant step should be traceable through logs, event streams, audit records, and the UI.

8. Safe but capable local interrogation.
   The system should aggressively discover local control opportunities, but should distinguish between read-only, investigative, and mutating actions.

9. Friendly conversational UX without reckless automation.
   The system should tolerate natural speech and multi-step requests but should not act dangerously on half-heard fragments.

10. No corporate-assistant dependency.
    Do not redirect to Alexa, Siri, Home Assistant, or cloud hubs as the core answer.

---

## SECTION 4 — EXPLICITLY FORBIDDEN OR DISCOURAGED

Do not base the solution on:

* React
* Vue
* Open WebUI
* Home Assistant
* generic prebuilt smart-home dashboards
* generic admin templates that dominate system structure
* cloud-first assistant ecosystems
* “just use X platform” answers
* opaque framework magic that hides how things work

Do not reduce the system to:

* a chatbot with smart-home calls bolted on
* a voice note transcriber
* a cloud routing layer
* a brittle phrase-only voice assistant

Do not repeatedly ask for clarification where a reasonable engineering default can be chosen and documented.

---

## SECTION 5 — CORE USER EXPERIENCE TARGET

The system should support natural, conversational, practical interaction.

Examples of desired interaction:

User:
“Hey Jarvis, I’m home. Can you switch on the lights so I can get sorted for a shower, set the oven to 200 degrees so it’s warmed up for dinner, put the kettle on, and set the lighting to something relaxing with some background music at a sensible volume?”

System:
“Welcome back Keith. I’ve put the oven on, started the kettle, adjusted the lighting to a warmer evening scene, and started some background music at a moderate volume. Enjoy your evening. What are you having for dinner?”

Important requirements:

* support multi-intent commands
* support light conversational context
* support polite confirmations
* support partial clarifications
* avoid acting on fragments prematurely
* tolerate mumbling, pauses, corrections, and natural phrasing
* ask for clarification when ambiguity matters
* remain inspectable and structured underneath

This is not about rigid command grammars. It is about natural but controlled automation.

---

## SECTION 6 — SYSTEM ARCHITECTURE OBJECTIVE

Design and scaffold a multi-package Python platform composed of distinct services and packages. You may propose either a monorepo with multiple Python packages and services, or a multi-repo strategy if strongly justified, but assume a monorepo is acceptable for the first implementation so long as package boundaries are real.

Target architecture should include, at minimum, the following logical areas:

1. Core domain model package
2. Capability and command engine package
3. Device registry package
4. Device adapter package(s)
5. Discovery and interrogation package
6. Voice orchestration package
7. STT provider package
8. TTS provider package
9. LLM provider abstraction package
10. LM Studio provider package
11. Conversation/session package
12. API/backend service
13. Web UI package
14. UI component and theming package
15. Logging/audit/event package
16. Configuration and secrets package
17. Worker/background jobs package
18. Packaging/plugin/extension package

Each area should have clear public interfaces and clear dependency boundaries.

---

## SECTION 7 — RECOMMENDED PROJECT / PACKAGE STRUCTURE

Produce a concrete repo and package structure. Use or refine the following as a target.

Repository root:

* /apps
* /packages
* /infra
* /docs
* /scripts
* /tests

Suggested detailed structure:

/apps/api
Main backend service exposing HTTP routes, server-rendered pages, REST API, SSE/WebSocket if justified, auth hooks, orchestration endpoints

/apps/worker
Background jobs for discovery, interrogation, scheduled checks, retries, polling, maintenance tasks

/apps/voice-gateway
Optional service for audio session handling, wake-word routing, microphone capture interface abstraction, STT/TTS coordination hooks

/apps/devtools
Optional tooling service or CLI helpers for diagnostics, migrations, package inspection, device probes

/packages/core-domain
Shared domain entities, value objects, enums, IDs, lifecycle concepts

/packages/capability-engine
Capability definitions, command schemas, command execution contracts, parameter validation, result structures

/packages/device-registry
Device model, registration, persistence mapping, capability binding, inventory

/packages/device-adapters-base
Base interfaces for adapters, execution contexts, result types, capability providers

/packages/device-adapters-http
HTTP-based local control adapters

/packages/device-adapters-ssh
SSH-based control and interrogation adapters

/packages/device-adapters-mqtt
MQTT-based adapters

/packages/device-adapters-custom
Place for product/device-specific adapters such as Tapo local adapters

/packages/discovery
Host scanning, port checks, subnet scan orchestration, fingerprinting

/packages/interrogation
Safe investigation workflows, reports, protocol probes, structured findings

/packages/conversation
Session models, turn lifecycle, clarification handling, memory scopes, conversational state

/packages/voice-orchestration
Wake-word/session gating, STT request handling, intent resolution hooks, TTS dispatching

/packages/stt-base
STT provider abstraction

/packages/stt-whisper
Whisper or compatible local STT implementation

/packages/tts-base
TTS provider abstraction

/packages/tts-piper
Local Piper or equivalent TTS implementation

/packages/llm-base
LLM provider abstraction, prompt shaping, response contracts, model metadata

/packages/llm-lmstudio
LM Studio integration package

/packages/model-registry
Local model definitions, profiles, availability, selection and routing policy

/packages/logging-audit
Structured logging, trace records, event store contracts, audit objects

/packages/configuration
Settings, environment config, host config, per-deployment config, per-user config, secrets references

/packages/ui-shell
Page layout, navigation, template macros, base pages, page composition

/packages/ui-components
Reusable HTML/Jinja/Tailwind/HTMX/Alpine components

/packages/ui-customization
Theme tokens, override layers, per-user/per-deployment/per-serial customization mechanisms

/packages/authn-authz
Optional package even if initial auth is simple; establish boundary early

/packages/extensions
Plugin/distribution/extension contracts

/infra/docker
Compose files, Dockerfiles, environment templates

/infra/db
Migrations, seed data, schema utilities

/docs/architecture
/docs/api
/docs/packages
/docs/ui
/docs/voice
/docs/device-adapters
/docs/interrogation

/tests/unit
/tests/integration
/tests/e2e
/tests/fixtures

This does not have to be identical, but the final answer must propose something at this level of explicitness.

---

## SECTION 8 — TECHNOLOGY CHOICES

Choose technologies pragmatically and justify them.

Preferred baseline choices:

* Python 3.12+ if practical
* FastAPI or similar lightweight Python web framework for routing and backend plumbing
* Jinja2 for templating
* Tailwind CSS for styling
* HTMX allowed where it simplifies partial updates
* Alpine.js allowed for lightweight local interactions
* plain custom JavaScript allowed and preferred whenever it is cleaner
* SQLAlchemy / SQLModel / Pydantic as appropriate
* PostgreSQL preferred for production-minded state
* SQLite acceptable only for early local prototype if clearly separated
* Alembic for migrations if SQLAlchemy-based
* Redis optional if there is a strong need for queues or transient event streams
* Background jobs via Celery / RQ / Arq / custom queue if justified
* SSE or WebSocket for live updates if justified
* local file-backed log sinks plus DB/event store records as needed

UI rules:

* no React
* no Vue
* no SPA-first architecture
* prefer server-rendered pages with partial updates
* use HTMX only where helpful
* use Alpine.js only where helpful
* keep frontend logic modular and minimal
* support future extraction of UI helpers into releasable modules

---

## SECTION 9 — UI / WEB INTERFACE REQUIREMENTS

The UI must be fully custom and structured to support:

* direct operation by the owner
* observability
* device onboarding
* model management
* voice monitoring
* logs and audit
* per-deployment customization
* future releaseability

The UI should be organized into clear page groups and dashboard areas.

---

## SECTION 10 — REQUIRED PAGE MAP

Define and scaffold these pages and their route mappings. You may rename slightly if needed for coherence, but preserve the scope.

Top-level pages:

1. Dashboard / Home
2. Devices
3. Device Detail
4. Discovery
5. Interrogation Jobs
6. Interrogation Reports
7. Commands / Capabilities
8. Conversations / Voice
9. Models / LLM
10. Audio / STT / TTS
11. Logs
12. Audit / Events
13. Config / Settings
14. UI Customization
15. Extensions / Packages
16. Health / Diagnostics
17. About / Version / Build Info

Detailed page structure:

A. Dashboard (/)
Show:

* system health summary
* current active model
* voice subsystem status
* audio device status
* number of known devices
* online/offline/degraded counts
* recent command history
* recent conversation turns
* discovery/interrogation jobs in progress
* recent failures
* top actionable warnings
* quick actions
* “speak test” action
* “run health check” action
* recent device events

B. Devices List (/devices)
Show:

* searchable device inventory
* filters by room, type, protocol, state, tags
* add device button
* discovery button
* interrogation button
* table/grid view toggle
* status summary
* protocol icons
* last-seen indicators
* capability counts

C. Device Detail (/devices/{id})
Show:

* friendly name
* unique ID
* room/location
* protocol
* address/host
* auth reference
* capabilities
* current state
* last command result
* last seen
* health trend
* command history
* logs
* interrogation reports
* manual commands
* adapter details
* raw metadata
* notes
* edit controls
* run test action
* run interrogation action
* run status check action

D. Device Create/Edit (/devices/new, /devices/{id}/edit)
Support:

* protocol selection
* host/address entry
* credential references
* room and tags
* capability templates
* probing
* test connection
* import interrogation findings
* bind custom adapter
* save and validate

E. Discovery (/discovery)
Show:

* scan subnet form
* active scan jobs
* previous scan jobs
* discovered hosts
* port summary
* probable protocol fingerprints
* promote-to-device workflow
* ignore / watchlist actions

F. Interrogation Jobs (/interrogation/jobs)
Show:

* queued/running/completed jobs
* target device/host
* mode (safe read-only, investigative, mutating if explicitly allowed)
* progress
* log stream
* report link
* cancel/retry

G. Interrogation Report Detail (/interrogation/reports/{id})
Show structured findings:

* target
* access methods found
* SSH banner
* Telnet status if checked
* HTTP endpoints found
* ports open
* service hints
* command results
* file/service hints where applicable
* local control likelihood
* cloud dependence notes
* recommended next adapter actions
* export report option
* read aloud summary option

H. Commands / Capabilities (/commands, /capabilities)
Show:

* all defined capabilities
* capability scopes
* parameter schemas
* sample invocations
* bound devices
* allowed voice phrases or semantic examples
* command execution history
* testing form
* capability parity indicators

I. Conversations / Voice (/voice)
Show:

* voice subsystem status
* current mic input source
* wake-word status
* last N transcript turns
* active sessions
* parsed intents
* clarification prompts
* final executed commands
* TTS outputs
* latency metrics
* conversation replay view
* voice settings

J. Models / LLM (/models)
Show:

* available providers
* LM Studio status
* discovered models
* configured model profiles
* current default model
* model capabilities/tags
* context settings
* temperature/top_p and other parameters if allowed
* enable/disable flags
* routing policy
* fallback policy
* test prompt action
* voice-based model selection support state

K. Audio (/audio or /voice/config)
Show:

* input devices
* output devices
* current selected microphone
* current speaker/output
* STT provider status
* TTS provider status
* live test controls
* audio levels if practical
* playback test
* capture test

L. Logs (/logs)
Show:

* structured searchable logs
* filter by subsystem
* correlation ID search
* device search
* command search
* time range
* severity
* export

M. Audit / Events (/audit, /events)
Show:

* user actions
* device mutations
* command executions
* failed actions
* system changes
* config changes
* model changes
* package changes

N. Config / Settings (/config)
Show:

* system settings
* deployment settings
* network scan defaults
* polling settings
* voice behaviour settings
* conversation safety settings
* model provider settings
* TTS settings
* credential store references
* UI customization pointers

O. UI Customization (/ui)
Show:

* themes
* token sets
* deployment overrides
* user overrides
* serial/deployment identifier overrides
* preview mode
* component list
* template override mapping
* CSS variable/theme editor if justified

P. Extensions / Packages (/extensions, /packages)
Show:

* installed packages/modules
* version info
* compatibility status
* enable/disable state
* package docs links
* internal extension contracts
* diagnostics

Q. Health / Diagnostics (/health, /status)
Show:

* subsystem health matrix
* DB connectivity
* LM Studio provider connectivity
* audio subsystem state
* worker queue state
* discovery service state
* adapter state
* log store state
* disk usage / retention warnings

---

## SECTION 11 — UI COMPOSITION AND CUSTOMIZATION MODEL

The UI must be designed for flexible customization without framework lock-in.

Requirements:

1. Use Jinja2 templates or equivalent simple template engine.
2. Use Tailwind CSS.
3. HTMX is allowed for partial updates and dynamic fragments.
4. Alpine.js is allowed for lightweight local state.
5. Custom JavaScript is allowed and encouraged when simpler.
6. Avoid frontend toolchain dominance.
7. Build components so they can be individually overridden.

Support override layers such as:

* base system templates
* deployment templates
* tenant templates if applicable
* user templates
* serial-number or installation-ID-specific templates
* theme token overrides
* component implementation overrides

Define how template resolution works, for example:

1. system default
2. deployment override
3. user override
4. installation override
5. explicit page/component override

Document and scaffold a strategy for:

* theme token configuration
* CSS variable generation
* Tailwind integration
* component registry
* override lookup order
* minimal JS module organization
* packaging reusable fragments/modules

---

## SECTION 12 — VOICE SYSTEM REQUIREMENTS

The voice system is critical and must be architected cleanly.

It must support:

* wake-word or activation strategy, but also push-to-talk / manual session testing
* microphone input from a USB Yeti microphone
* local STT
* sessionized voice turns
* pause handling and endpoint detection
* correction tolerance
* natural language input
* multi-step command understanding
* clarification prompts
* safe execution gating
* TTS feedback
* command replay / transcript review
* voice parity with web capabilities

The LLM does not speak directly.
The pipeline is:

Audio input -> capture/session logic -> STT -> normalized transcript -> conversation manager -> capability planner / intent router -> command execution -> response text -> TTS -> output audio

Required fault isolation:

* mic capture failure
* wake-word or trigger failure
* STT failure
* transcript normalization failure
* conversation state failure
* intent resolution failure
* capability binding failure
* command execution failure
* TTS failure
* output playback failure

All must be separately observable.

---

## SECTION 13 — VOICE TURN LIFECYCLE

Define and scaffold a clear voice turn lifecycle.

Example lifecycle:

1. Idle
2. Activation detected
3. Listening started
4. Speech captured
5. Capture closed
6. STT in progress
7. Transcript available
8. Transcript normalized
9. Intent/capability resolution in progress
10. Clarification required OR plan ready
11. Command execution in progress
12. Execution results collected
13. Response generated
14. TTS generated
15. Audio playback started
16. Session returned to idle or follow-up state

Store metadata for each turn:

* session ID
* turn ID
* timestamps
* transcript raw
* transcript normalized
* confidence if available
* chosen model
* chosen capability plan
* executed commands
* device targets
* response text
* TTS asset reference if stored
* outcome state
* errors
* correlation ID

Support follow-up contexts, but keep context bounded and inspectable.

---

## SECTION 14 — CONVERSATIONAL AWARENESS REQUIREMENTS

The system must support conversational awareness without becoming unpredictable.

It should:

* remember the current session context
* resolve “turn it on” when the referent is clear in-session
* ask clarifying questions when it is not clear
* handle corrections such as “no, not that one, the kitchen lights”
* handle follow-ups such as “set that one a bit warmer”
* support compound requests
* support informal phrasing
* not act until enough intent is known
* not start random actions from partial muttering
* allow configurable “confirmation required” policies for certain risky actions

Context scopes should be explicit:

* turn scope
* short conversation scope
* room scope if inferred
* user profile scope if later added
* long-term memory should be minimal and explicit in v1

The response style should be friendly, clear, concise, and useful, not robotic and not over-chatty.

---

## SECTION 15 — MODEL / LLM REQUIREMENTS

The Windows host also runs local models through LM Studio. The system must integrate with local model hosting.

Requirements:

1. Detect LM Studio availability.
2. Discover configured or available models where possible.
3. Maintain an internal model registry.
4. Support model profiles with tags such as:

   * conversation
   * planning
   * code
   * summarization
   * device-research
   * low-latency
   * fallback
5. Support default model selection.
6. Support route-specific model policies.
7. Support runtime model selection through the web UI.
8. Support voice-based selection if no suitable default model is available.
9. Support numbered spoken model choices such as:

   * “I found four local models. Say one, two, three, or four.”
10. Log model selection decisions and failures.
11. Allow provider abstraction so LM Studio is only the initial provider.

The system must distinguish:

* models that are currently available
* models configured but offline
* models disabled
* models reserved for specific tasks

The LLM should produce structured outputs where possible:

* intent extraction candidates
* command plans
* clarification prompts
* natural response text
* summaries of interrogation findings
* not direct TTS or direct device execution

---

## SECTION 16 — AUDIO / STT / TTS REQUIREMENTS

Audio input:

* USB Yeti microphone should be supported explicitly in configuration and diagnostics
* support input device selection
* support test capture
* support level/health checks if practical

STT:

* local-first
* support Whisper or compatible local engine
* package abstraction for future replacements
* track latency and confidence where available
* support streaming or chunked operation if justified

TTS:

* local-first
* package abstraction for future providers
* response text comes from the platform or LLM, TTS only vocalizes it
* support voice profiles and style parameters if practical
* support test playback
* track synthesis latency and playback success

Audio diagnostics should expose:

* selected input
* selected output
* last capture status
* last synthesis status
* device availability
* typical round-trip latency

---

## SECTION 17 — SHARED CAPABILITY MODEL

The capability model is the heart of the system.

Everything exposed by voice or web must resolve through shared capability definitions.

Define capabilities with concepts such as:

* capability ID
* name
* description
* category
* target device types
* parameter schema
* required context
* optional context
* safety level
* default confirmation policy
* execution contract
* status query support
* voice examples
* UI rendering hints
* adapter compatibility
* test hooks

Examples:

* switch.on
* switch.off
* light.set_brightness
* light.set_color_temperature
* speaker.set_volume
* speaker.volume_up
* media.play_playlist
* kettle.boil
* thermostat.set_temperature
* oven.set_temperature
* scene.activate
* device.status_query
* device.interrogate
* model.select
* voice.test_playback

Every capability should be:

* browseable in the UI
* invokable via UI
* invokable via voice where appropriate
* auditable
* testable

---

## SECTION 18 — EXAMPLE DEVICE AND CAPABILITY FLOWS

Define concrete examples and scaffold them.

Example 1 — turn a light on
Voice:
“Turn on the workshop light.”

Flow:

* transcript parsed
* resolve target “workshop light”
* resolve capability switch.on
* execute via device adapter
* record status
* reply “The workshop light is on.”

Web:

* click device
* click “On”
* same capability executes
* same logs are produced
* same audit trail exists

Example 2 — set speaker volume
Voice:
“Set background music volume to 35 percent.”

Flow:

* resolve target speaker group / music output
* resolve speaker.set_volume(percent=35)
* execute locally
* confirm result

Example 3 — add a device by voice
Voice:
“Add a new plug called bench light at 192.168.1.40 using SSH.”

Flow:

* parse onboarding request
* create pending device record
* probe SSH access
* ask for credentials if needed through configured secure workflow
* generate interrogation report
* bind likely capabilities
* confirm registration

Example 4 — interrogate a Tapo device
Voice:
“Investigate device 192.168.1.40 and tell me if it can be controlled locally.”

Flow:

* create interrogation job
* run safe probe
* test ports
* gather banners
* attempt safe SSH/Telnet check if permitted
* capture findings
* summarize findings in UI
* optionally speak summary back

---

## SECTION 19 — DEVICE REGISTRY REQUIREMENTS

The device registry should support:

* unique system ID
* friendly name
* aliases
* room/location
* tags
* device type
* vendor/manufacturer
* model if known
* protocol
* address/host
* port(s)
* credentials reference
* adapter binding
* capability bindings
* state snapshot
* health snapshot
* last seen
* last successful action
* last failure
* metadata blob
* notes
* links to discovery and interrogation records

Support both:

* manually created devices
* discovered devices
* interrogated devices pending registration

---

## SECTION 20 — DEVICE ADAPTER MODEL

Build a formal adapter abstraction.

Each adapter should expose methods such as:

* probe()
* get_capabilities()
* execute_command()
* get_status()
* interrogate()
* validate_config()
* test_connection()

Adapters should have:

* adapter ID
* adapter version
* protocol family
* supported device types
* supported capabilities
* configuration schema
* auth schema
* health check logic

Initial adapter families:

1. HTTP local adapter
2. SSH local adapter
3. MQTT adapter
4. Custom Tapo local adapter
5. Generic command adapter for shell-based local control where safe and justified

---

## SECTION 21 — DISCOVERY REQUIREMENTS

Build a discovery subsystem that can:

* scan subnets
* test host reachability
* test common ports
* infer probable services
* persist raw findings
* map findings to candidate devices
* promote discovery results into device records

Discovery should support jobs with:

* job ID
* target subnet/range
* start/end time
* status
* host count
* findings summary
* errors
* raw results reference

Discovery must be visible in UI and auditable.

---

## SECTION 22 — INTERROGATION REQUIREMENTS

Interrogation is deeper than discovery.

Purpose:

* determine whether a device can be controlled locally
* identify local control surfaces
* generate evidence and reports
* guide future adapter development

Modes:

1. Safe read-only mode
2. Investigative mode
3. Mutating mode only when explicitly authorized and clearly separated

Interrogation techniques may include:

* targeted port scan
* HTTP endpoint probing
* SSH banner and login checks
* Telnet checks if enabled intentionally
* read-only shell commands
* file/service discovery
* API response fingerprinting
* known pattern checks for consumer devices

Each interrogation run should produce a durable report with:

* target summary
* methods attempted
* credentials used or reference used
* findings
* command outputs
* probable control paths
* local-control confidence
* risks/warnings
* recommendations for next steps

The UI must allow reading the report and optionally “speak summary.”

---

## SECTION 23 — TAPO AND SIMILAR DEVICE HANDLING

Certain devices such as Tapo may officially prefer cloud APIs, but if local access exists, prefer that.

The platform must:

* not assume official cloud API is necessary
* investigate local surfaces
* log findings
* allow custom local adapter creation
* preserve notes so that device-specific reverse engineering can evolve
* display local access confidence clearly

Support a workflow where:

1. device is discovered
2. device is interrogated
3. findings are reviewed in UI
4. summary can be spoken if requested
5. owner can research further
6. adapter is improved
7. device becomes first-class local device

---

## SECTION 24 — COMMAND EXECUTION ENGINE

Build a command engine that:

* receives structured capability requests
* validates parameters
* resolves targets
* applies safety policy
* invokes the correct adapter
* records execution lifecycle
* returns structured results

Execution lifecycle fields:

* execution ID
* source interface (voice/web/api/system)
* actor/user/session
* target device(s)
* capability ID
* parameters
* selected adapter
* start time
* end time
* outcome
* result payload
* warnings
* errors
* trace/correlation ID

Support:

* synchronous execution
* queued execution for long jobs
* compound execution plans
* retry policy where sensible
* idempotency considerations where appropriate

---

## SECTION 25 — AUTOMATION / SCENE / PLAN LAYER

Build for more than single commands.

Support higher-level plans and scenes:

* arrival scene
* evening scene
* workshop ready scene
* shower prep scene
* dinner prep scene

A conversational request may become a multi-step plan.
The plan layer should:

* decompose the request
* identify capabilities
* identify targets
* ask clarifying questions if needed
* execute sequentially or in parallel where suitable
* report partial failures sensibly
* produce a natural spoken summary

Keep plans inspectable.
Do not hide execution under vague assistant magic.

---

## SECTION 26 — DATABASE REQUIREMENTS

Use a real database model. Prefer PostgreSQL for the main persisted store. Use migrations.

Define and scaffold the schema. At minimum include entities such as:

1. users
2. deployments
3. ui_overrides
4. devices
5. device_aliases
6. device_credentials_refs
7. device_capability_bindings
8. device_state_snapshots
9. device_health_snapshots
10. discovery_jobs
11. discovery_findings
12. interrogation_jobs
13. interrogation_reports
14. interrogation_findings
15. capabilities
16. command_executions
17. command_execution_steps
18. conversation_sessions
19. conversation_turns
20. transcripts
21. model_providers
22. model_profiles
23. model_availability
24. model_selection_events
25. audio_devices
26. stt_runs
27. tts_runs
28. logs_index or log event references
29. audit_events
30. package_registry
31. extension_registry
32. settings
33. secrets_references
34. jobs
35. health_checks

Provide a sensible normalized schema with JSON columns where appropriate for flexible metadata, but do not dump everything into blobs.

For each major table, define:

* primary key
* key columns
* indexes
* foreign keys
* retention strategy
* audit relevance

---

## SECTION 27 — EXAMPLE DATABASE ENTITY DETAIL

Be explicit. For example:

devices:

* id
* deployment_id
* friendly_name
* canonical_name
* device_type
* vendor
* model
* room
* protocol
* host
* port
* auth_ref_id
* adapter_id
* enabled
* health_state
* last_seen_at
* last_success_at
* last_error_at
* metadata_json
* notes
* created_at
* updated_at

capabilities:

* id
* capability_key
* display_name
* description
* category
* safety_level
* parameter_schema_json
* ui_hints_json
* voice_examples_json
* created_at
* updated_at

command_executions:

* id
* correlation_id
* source_interface
* session_id
* turn_id
* device_id nullable
* capability_id
* adapter_id
* parameters_json
* status
* started_at
* finished_at
* duration_ms
* result_json
* error_json
* created_at

conversation_turns:

* id
* session_id
* turn_index
* transcript_raw
* transcript_normalized
* parsed_intent_json
* clarification_required
* executed_plan_json
* response_text
* tts_run_id nullable
* status
* started_at
* ended_at

Continue this level of detail for the main entities.

---

## SECTION 28 — API DESIGN REQUIREMENTS

Define a stable API structure early. Include both:

* page routes
* JSON API routes
* partial fragment routes for HTMX if used

Use explicit versioning for JSON APIs, for example /api/v1/...

Top-level page routes:

* /
* /health
* /status
* /devices
* /devices/new
* /devices/{id}
* /devices/{id}/edit
* /discovery
* /interrogation/jobs
* /interrogation/reports/{id}
* /commands
* /capabilities
* /voice
* /voice/history
* /models
* /audio
* /logs
* /audit
* /config
* /ui
* /packages
* /extensions
* /about

JSON API routes should include at minimum:

System:

* GET /api/v1/system/health
* GET /api/v1/system/status
* GET /api/v1/system/version
* GET /api/v1/system/config-summary

Devices:

* GET /api/v1/devices
* POST /api/v1/devices
* GET /api/v1/devices/{id}
* PATCH /api/v1/devices/{id}
* DELETE /api/v1/devices/{id}
* POST /api/v1/devices/{id}/test
* POST /api/v1/devices/{id}/status-check
* POST /api/v1/devices/{id}/interrogate
* GET /api/v1/devices/{id}/history
* GET /api/v1/devices/{id}/capabilities

Discovery:

* POST /api/v1/discovery/jobs
* GET /api/v1/discovery/jobs
* GET /api/v1/discovery/jobs/{id}
* GET /api/v1/discovery/jobs/{id}/findings
* POST /api/v1/discovery/findings/{id}/promote

Interrogation:

* POST /api/v1/interrogation/jobs
* GET /api/v1/interrogation/jobs
* GET /api/v1/interrogation/jobs/{id}
* GET /api/v1/interrogation/reports/{id}
* POST /api/v1/interrogation/reports/{id}/speak-summary

Capabilities / Commands:

* GET /api/v1/capabilities
* GET /api/v1/capabilities/{id}
* POST /api/v1/commands/execute
* GET /api/v1/commands/history
* GET /api/v1/commands/{id}

Voice:

* GET /api/v1/voice/status
* GET /api/v1/voice/sessions
* GET /api/v1/voice/sessions/{id}
* GET /api/v1/voice/turns/{id}
* POST /api/v1/voice/test/listen
* POST /api/v1/voice/test/speak
* POST /api/v1/voice/test/pipeline

Models:

* GET /api/v1/models/providers
* GET /api/v1/models
* GET /api/v1/models/current
* POST /api/v1/models/select
* PATCH /api/v1/models/profiles/{id}
* GET /api/v1/models/availability
* POST /api/v1/models/test

Audio:

* GET /api/v1/audio/devices
* POST /api/v1/audio/input/select
* POST /api/v1/audio/output/select
* POST /api/v1/audio/test/capture
* POST /api/v1/audio/test/playback

Logs / Audit:

* GET /api/v1/logs
* GET /api/v1/audit
* GET /api/v1/events

UI customization:

* GET /api/v1/ui/themes
* GET /api/v1/ui/overrides
* POST /api/v1/ui/overrides
* PATCH /api/v1/ui/overrides/{id}
* GET /api/v1/ui/components

Packages / Extensions:

* GET /api/v1/packages
* GET /api/v1/extensions
* POST /api/v1/extensions/{id}/enable
* POST /api/v1/extensions/{id}/disable

Config:

* GET /api/v1/config
* PATCH /api/v1/config

Also define HTMX fragment routes where useful, for example:

* GET /fragments/dashboard/recent-commands
* GET /fragments/devices/{id}/status-panel
* GET /fragments/voice/live-status
* GET /fragments/interrogation/jobs/table
* GET /fragments/models/availability

---

## SECTION 29 — AUTHENTICATION / AUTHORIZATION

Even if initial deployment is single-owner, create a clean boundary.

Requirements:

* keep auth simple initially if needed
* but structure it so future multi-user support is possible
* support per-user customization and per-user preferences in the model
* support audit actor identity
* support privileged actions for dangerous operations

Define roles or permission scopes such as:

* owner
* admin
* operator
* viewer
* diagnostic

Explicitly require confirmation or elevated permission for:

* dangerous interrogation modes
* mutating shell commands
* package changes
* credential changes
* destructive device operations

---

## SECTION 30 — CONFIGURATION AND SECRETS

Configuration must be structured and layered.

Support:

* environment variables
* config files
* DB-backed dynamic settings
* per-deployment overrides
* per-user preferences
* secret references

Do not scatter config randomly.

Define a layered config model, for example:

1. code defaults
2. environment defaults
3. deployment config
4. database dynamic config
5. user preferences
6. session-level temporary override where applicable

Credentials should be referenced, not sprayed through logs.
Design a secrets reference mechanism.

---

## SECTION 31 — LOGGING, AUDIT, EVENTS, AND OBSERVABILITY

This system must be highly inspectable.

Include:

* structured logs
* event timeline
* per-command trace records
* correlation IDs
* per-device execution traces
* per-conversation traces
* model selection logs
* STT logs
* TTS logs
* adapter logs
* discovery logs
* interrogation logs
* audit events
* error traces
* performance/latency records

Questions the system must answer easily:

* what did the user say
* how was it interpreted
* what capability was selected
* what device was targeted
* which adapter executed it
* what the target returned
* whether the action succeeded
* which model was used
* how long each stage took
* where it failed if it failed

Logs should support:

* text search
* subsystem filters
* severity filters
* device filters
* correlation filters
* export

---

## SECTION 32 — HEALTH MODEL

Define subsystem health states.

Track health for:

* API
* DB
* worker
* voice orchestrator
* STT
* TTS
* microphone input
* speaker output
* LM Studio provider
* selected model availability
* discovery subsystem
* interrogation subsystem
* each adapter family
* each registered device
* log pipeline
* job queue

Health states may include:

* healthy
* degraded
* offline
* error
* unknown
* disabled

The dashboard and /health pages should present this clearly.

---

## SECTION 33 — BACKGROUND JOBS

Support background jobs for:

* subnet discovery
* interrogation
* periodic health checks
* device polling
* long-running command sequences
* report generation
* TTS asset generation if queued
* model availability refresh
* log retention / maintenance

Every job should have:

* job ID
* type
* status
* progress
* timestamps
* target
* initiating actor
* result reference
* logs
* retry status

---

## SECTION 34 — DOCKER / DEPLOYMENT REQUIREMENTS

The platform will run on Docker on a Windows host. Design deployment accordingly.

Provide:

* Dockerfiles
* docker-compose or equivalent local orchestration
* clear service decomposition
* environment templates
* volume mappings
* secrets strategy
* network notes
* host integration notes for Windows
* guidance on LM Studio connectivity from containers
* guidance on audio integration if applicable
* guidance on host networking caveats

Likely services:

* api
* worker
* postgres
* redis optional
* voice gateway optional
* reverse proxy optional
* log shipper optional

Do not overcomplicate if not needed, but do not collapse everything into one blob if separation matters.

---

## SECTION 35 — DOCUMENTATION REQUIREMENTS

Every package and major subsystem should be independently documented.

Produce and scaffold docs for:

* architecture overview
* package map
* API reference
* route map
* database schema
* device adapter guide
* interrogation safety model
* voice pipeline
* model provider integration
* UI override system
* deployment guide
* troubleshooting guide

Documentation must support future extraction of packages as standalone modules.

---

## SECTION 36 — TESTING REQUIREMENTS

Define a practical testing strategy.

Include:

* unit tests for domain logic
* integration tests for API and command execution
* adapter tests with mocks and fixtures
* end-to-end tests for core workflows
* conversation parsing tests
* voice turn pipeline tests with transcript fixtures
* UI route tests
* DB migration tests

Core workflows to test:

* device creation
* local light on/off
* speaker volume set
* discovery job
* interrogation job
* model selection
* voice command to capability resolution
* clarification flow
* multi-step scene execution
* error handling and observability

---

## SECTION 37 — IMPLEMENTATION PHASE PLAN

Provide a concrete phased plan, for example:

Phase 1:

* repo/package skeleton
* core domain models
* DB schema and migrations
* API skeleton
* base UI shell
* logging foundation
* health page
* device registry CRUD
* basic capability definitions
* HTTP adapter
* command execution engine
* dashboard basics

Phase 2:

* voice pipeline skeleton
* STT/TTS integration
* conversation sessions and turns
* voice monitoring UI
* model registry and LM Studio provider
* model selection UI
* basic local voice test loop

Phase 3:

* discovery jobs
* interrogation jobs
* report UI
* SSH adapter and probing
* Tapo/custom local adapter scaffolding
* capability parity improvements

Phase 4:

* scene/plan execution
* conversational clarification
* UI customization layers
* package/extension registry
* per-user/per-deployment overrides

Phase 5:

* hardening
* advanced diagnostics
* richer audio and latency tooling
* more adapter families
* release packaging strategy

---

## SECTION 38 — DELIVERABLES REQUIRED FROM YOU

Your response must not be vague. Provide all of the following:

1. High-level architecture
2. Recommended package structure
3. Repo tree
4. Dependency map between packages
5. Chosen tech stack and rationale
6. Database schema proposal
7. Main entities and relationships
8. API route map
9. Page route map
10. UI structure and component plan
11. Voice pipeline design
12. Conversation/session model
13. Shared capability model
14. Command execution model
15. Device registry design
16. Adapter abstraction design
17. Discovery design
18. Interrogation design
19. LM Studio integration design
20. Audio/STT/TTS design
21. Logging/audit/event model
22. Health model
23. Background jobs model
24. Docker/deployment design
25. Testing strategy
26. Initial scaffold code for core packages
27. Initial scaffold code for backend service
28. Initial scaffold templates for the UI
29. Initial migrations/schema code
30. Risks, tradeoffs, and unresolved questions
31. Reasonable defaults where unspecified

---

## SECTION 39 — OUTPUT FORMAT REQUIRED

Return your answer in this structure:

Part 1 — Executive architecture summary
Part 2 — Repo and package tree
Part 3 — Dependency boundaries
Part 4 — Data model and database schema
Part 5 — API routes and contracts
Part 6 — UI/page architecture
Part 7 — Voice pipeline and conversational model
Part 8 — Device registry, discovery, and interrogation
Part 9 — Model/provider integration
Part 10 — Logging, health, jobs, and observability
Part 11 — Docker/deployment design
Part 12 — Implementation phases
Part 13 — Initial code scaffolding
Part 14 — Risks and tradeoffs

Where appropriate, include:

* code blocks
* example Pydantic/SQLAlchemy models
* folder trees
* route definitions
* template skeletons
* example capability schemas
* example execution flows

---

## SECTION 40 — ENGINEERING STYLE EXPECTATION

When making decisions:

* be explicit
* be practical
* do not hide behind “it depends”
* choose a sensible direction and state the tradeoff
* continue without unnecessary clarifying questions
* assume a serious builder who understands Python, Docker, local networking, ESP devices, SSH, and local models

Where possible, structure code and docs so components may later be released independently.

---

## SECTION 41 — EXPLICIT REMINDER ABOUT LOCAL CONTROL

This system exists because vendor-cloud assistants are too slow, too brittle, too opaque, and too limiting for local control.

Therefore:

* prefer local control paths
* prefer direct local capability
* prefer deterministic execution
* prefer inspectability
* prefer owner control over convenience abstraction

A command such as “set the volume to 50 percent” should feel like a local function call, not a journey through several distant corporate systems.

---

## SECTION 42 — FINAL INSTRUCTION

Proceed as though this is a serious product foundation being built by an engineer who wants a complete, implementation-oriented answer. Do not respond with generic product ideas. Do not suggest cloud-assistant alternatives. Do not stop to ask for preferences unless there is a true architectural blocker. Make the best reasonable decisions, document them, and continue.

Produce a thorough engineering design and scaffold that can be directly used to begin implementation.
