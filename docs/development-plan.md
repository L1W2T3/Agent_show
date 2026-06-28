# AI Backend Architect — Development Plan

## 1. Delivery Strategy

Build the system incrementally while preserving Clean Architecture boundaries. Each phase should produce working, tested slices without prematurely coupling domain logic to FastAPI, LangGraph, SQLAlchemy, Redis, or LLM SDKs.

## 2. Milestones

### Milestone 1 — Architecture Foundation

Status: current planning phase.

Deliverables:

- `docs/architecture.md`
- `docs/development-plan.md`
- Target directory tree
- Module responsibility definitions

Acceptance criteria:

- Architecture explains backend, frontend, LLM, persistence, cache, and workflow boundaries.
- Development plan defines implementation order.
- No new implementation code is introduced in this phase.

### Milestone 2 — Domain Model

Deliverables:

- Domain entities and value objects for design tasks and generated artifacts.
- Domain events for task lifecycle changes.
- Domain exceptions.
- Unit tests.

Acceptance criteria:

- Domain imports no infrastructure or framework packages.
- Domain tests run without PostgreSQL, Redis, FastAPI, or LangGraph.
- Invariants are enforced in entities/value objects.

### Milestone 3 — Application Layer

Deliverables:

- Use cases:
  - Submit design task.
  - Get design task status.
  - Get design task result.
- Application DTOs.
- Ports:
  - Task repository.
  - Artifact repository.
  - Unit of work.
  - Cache.
  - LLM gateway.
  - Workflow runner.
- Unit tests with fakes.

Acceptance criteria:

- Use cases depend on ports, not concrete infrastructure.
- Use cases are async.
- Tests do not require external services.

### Milestone 4 — FastAPI Presentation Layer

Deliverables:

- FastAPI application factory.
- API versioning.
- Endpoints:
  - `POST /design`
  - `GET /tasks/{id}`
  - `GET /tasks/{id}/result`
- Request and response schemas.
- Exception handlers.
- OpenAPI metadata.
- Integration tests.

Acceptance criteria:

- Request validation is enforced.
- Response models are validated.
- Application errors map to correct HTTP responses.
- Dependencies can be overridden in tests.

### Milestone 5 — LLM Abstraction

Deliverables:

- OpenAI-compatible LLM gateway.
- Provider configuration for OpenAI, Qwen, DeepSeek, and custom compatible APIs.
- Structured output parser.
- Retry and timeout policy.
- Unit tests with mocked provider responses.

Acceptance criteria:

- Application code does not depend on provider SDKs.
- Provider can be switched through configuration.
- Structured output failures are handled explicitly.

### Milestone 6 — LangGraph Workflow

Deliverables:

- Shared graph state.
- Agent nodes:
  - Requirement Agent.
  - Domain Agent.
  - Architecture Agent.
  - Database Agent.
  - API Agent.
  - Infrastructure Agent.
  - Review Agent.
- Prompt templates.
- Retry policy.
- Error handling.
- Workflow tests.

Acceptance criteria:

- Each node has a typed input/output contract.
- Graph execution is async.
- Node failures are observable and retryable.
- Final result is deterministic in shape.

### Milestone 7 — Persistence and Migrations

Deliverables:

- SQLAlchemy async engine/session management.
- ORM models for tasks, artifacts, and workflow events.
- Repository implementations.
- Alembic setup and initial migrations.
- Integration tests against PostgreSQL.

Acceptance criteria:

- All persisted records have timestamps.
- JSON artifacts are versioned.
- Repository tests validate round-trips.
- Migrations can upgrade and downgrade cleanly.

### Milestone 8 — Redis Integration

Deliverables:

- Redis cache adapter.
- Task status cache.
- Idempotency key support.
- Rate-limit primitive.
- Integration tests.

Acceptance criteria:

- Cache failures do not corrupt durable state.
- TTLs are explicit.
- Redis keys follow a documented naming convention.

### Milestone 9 — Frontend

Deliverables:

- Next.js application.
- Tailwind styling.
- Prompt submission page.
- Task progress UI.
- Architecture result viewer.
- Error states.

Acceptance criteria:

- UI can submit prompts and poll task status.
- UI renders each generated architecture section.
- UI handles pending, running, completed, and failed states.

### Milestone 10 — Production Hardening

Deliverables:

- Dockerfiles.
- Docker Compose.
- CI workflow.
- Logging configuration.
- Metrics/tracing hooks.
- Security review.
- Load-test plan.

Acceptance criteria:

- CI runs tests, linting, type checks, and migration checks.
- Local development starts with one command.
- Secrets are not committed.
- Operational runbook exists.

## 3. Suggested Implementation Order

1. Refine domain model for full architecture package lifecycle.
2. Add application ports and use cases.
3. Add FastAPI endpoints against fake/in-memory application services.
4. Add LLM gateway behind a port.
5. Add LangGraph state and nodes using fake LLM responses first.
6. Add PostgreSQL persistence.
7. Add Redis cache and rate limiting.
8. Replace fake workflow with real LLM-backed graph.
9. Add frontend.
10. Harden deployment and observability.

## 4. Testing Plan

### Unit Tests

- Domain entities and value objects.
- Application use cases with fake ports.
- Prompt rendering helpers.
- Structured output parsers.
- Workflow node logic with fake LLMs.

### Integration Tests

- FastAPI routes with dependency overrides.
- SQLAlchemy repositories with PostgreSQL.
- Alembic migrations.
- Redis cache adapter.
- OpenAI-compatible gateway with mocked HTTP transport.
- LangGraph workflow with deterministic fake agents.

### End-to-End Tests

- Submit design task.
- Poll task status.
- Fetch generated result.
- Render result in frontend.

## 5. Quality Gates

Before merging implementation phases:

- `pytest` passes.
- Type checking passes.
- Linting passes.
- Formatting check passes.
- Alembic migration check passes when persistence changes.
- No infrastructure dependency leaks into domain code.
- Public APIs have request and response validation.

## 6. Configuration Plan

Environment variables:

```text
APP_ENV=local
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
LLM_PROVIDER=openai
LLM_API_KEY=...
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4.1-mini
LLM_TIMEOUT_SECONDS=60
LLM_MAX_RETRIES=3
```

Provider-specific overrides should be supported:

```text
OPENAI_API_KEY=...
OPENAI_MODEL=...
QWEN_API_KEY=...
QWEN_MODEL=...
DEEPSEEK_API_KEY=...
DEEPSEEK_MODEL=...
```

## 7. Risk Register

### Risk: LLM output inconsistency

Mitigation:

- Use structured output schemas.
- Validate every agent output.
- Retry with corrective prompts.
- Review final package with Review Agent.

### Risk: Long-running requests

Mitigation:

- Treat design generation as asynchronous task processing.
- Return task ID immediately.
- Poll status/result endpoints.
- Move workflow execution to background workers when needed.

### Risk: Provider lock-in

Mitigation:

- Use OpenAI-compatible abstraction.
- Keep provider SDKs out of application/domain layers.
- Configure provider through environment.

### Risk: Architecture sections become inconsistent

Mitigation:

- Pass prior sections through shared graph state.
- Add cross-section validation in Review Agent.
- Persist versioned artifacts.

### Risk: Persistence schema changes quickly

Mitigation:

- Store generated sections as JSON artifacts initially.
- Normalize only stable query patterns later.
- Maintain Alembic migrations from the start.

## 8. Non-Goals for Initial Implementation

- Multi-user authentication.
- Billing.
- Real-time collaborative editing.
- Diagram rendering.
- Multi-tenant RBAC.
- Background worker scaling beyond a single process.

These can be introduced after the core architecture generation loop is stable.
