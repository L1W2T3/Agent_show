# AI Backend Architect — Complete Architecture

## 1. Product Vision

AI Backend Architect is a production-grade AI Solution Architect system. A user describes a backend system in natural language, and the platform generates a structured architecture package covering requirements, domain model, services, database design, API design, infrastructure, deployment, and review.

Example inputs:

- `Design a food delivery platform.`
- `Design a flash-sale e-commerce system.`
- `Design a SaaS CRM.`

The system should behave like a senior backend architect: it should ask architectural questions implicitly, infer constraints, reason through trade-offs, produce consistent artifacts, and review its own output for completeness and risk.

## 2. Target Outputs

For each design task, the agent generates:

1. Requirement Analysis
2. Domain Model
3. Service Decomposition
4. Database Design
5. API Design
6. Infrastructure Design
7. Deployment Design
8. Architecture Review

Each output should be structured, versionable, persisted, and available through APIs for frontend rendering and export.

## 3. Technology Stack

### Backend

- Python 3.12
- FastAPI
- LangGraph
- PostgreSQL
- Redis
- SQLAlchemy 2.x async ORM
- Alembic
- Pydantic v2
- OpenAI-compatible LLM APIs

### Frontend

- Next.js
- Tailwind CSS

### Runtime and Operations

- Docker
- Docker Compose for local development
- Kubernetes-ready deployment model
- Structured logging
- Metrics and tracing hooks
- CI checks for tests, linting, type checking, and migrations

## 4. Architectural Principles

### Clean Architecture

Dependencies must point inward:

```text
Presentation  ──> Application ──> Domain
Infrastructure ─> Application ──> Domain
Bootstrap      ─> Presentation + Application + Infrastructure
```

Rules:

- Domain code must not import FastAPI, SQLAlchemy, Redis, LangGraph, OpenAI SDKs, or framework-specific types.
- Application code orchestrates use cases and depends on domain objects plus abstract ports.
- Infrastructure code implements application ports.
- Presentation code translates HTTP requests/responses into application DTOs.
- Bootstrap code composes concrete dependencies.

### Domain-Driven Design

Primary bounded context:

```text
Architecture Design Generation
```

Core aggregate candidates:

- `DesignTask`
- `ArchitecturePackage`
- `RequirementAnalysis`
- `DomainModel`
- `ServiceDecomposition`
- `DatabaseDesign`
- `ApiDesign`
- `InfrastructureDesign`
- `DeploymentDesign`
- `ArchitectureReview`

DDD expectations:

- Domain invariants live in domain entities/value objects.
- Generated artifacts belong to a design task.
- A design task has a lifecycle and cannot be marked completed until required sections exist.
- Review findings should reference generated sections and severity.
- Value objects represent names, descriptions, identifiers, statuses, endpoint definitions, database columns, and deployment targets.

### Async First

- FastAPI endpoints are async.
- Database access uses SQLAlchemy async sessions.
- Redis access uses async clients.
- LLM calls are async.
- LangGraph execution is async.
- Blocking operations are isolated behind infrastructure adapters.

### Testability

- Application use cases depend on ports and can be tested with in-memory fakes.
- Domain tests do not require infrastructure.
- API tests override dependencies.
- LangGraph nodes are individually testable.
- Repository implementations are integration-tested against PostgreSQL.
- Cache implementations are integration-tested against Redis.

## 5. Agent Workflow

The architecture generation graph runs as a deterministic multi-step workflow with shared typed state.

```text
START
  ↓
Requirement Agent
  ↓
Domain Agent
  ↓
Architecture Agent
  ↓
Database Agent
  ↓
API Agent
  ↓
Infrastructure Agent
  ↓
Review Agent
  ↓
END
```

### Workflow Responsibilities

#### Requirement Agent

Produces requirement analysis from the user's natural-language prompt.

Responsibilities:

- Identify functional requirements.
- Identify non-functional requirements.
- Infer business assumptions.
- Identify actors and workflows.
- Identify constraints and risks.

#### Domain Agent

Produces a DDD-oriented domain model.

Responsibilities:

- Identify bounded contexts.
- Identify aggregates, entities, value objects, and domain services.
- Define domain events.
- Describe invariants.
- Map requirements to domain concepts.

#### Architecture Agent

Produces high-level system architecture and service decomposition.

Responsibilities:

- Choose monolith, modular monolith, microservices, or hybrid architecture.
- Define service boundaries.
- Define synchronous and asynchronous communication patterns.
- Identify external integrations.
- Explain trade-offs.

#### Database Agent

Produces persistence architecture.

Responsibilities:

- Design PostgreSQL schemas.
- Define tables, columns, indexes, constraints, and relationships.
- Identify transaction boundaries.
- Identify read/write patterns.
- Recommend caching strategy with Redis.

#### API Agent

Produces API design.

Responsibilities:

- Define REST endpoints.
- Define request and response schemas.
- Define validation rules.
- Define error contracts.
- Identify authentication and authorization boundaries.

#### Infrastructure Agent

Produces infrastructure and deployment architecture.

Responsibilities:

- Define backend runtime topology.
- Define frontend hosting topology.
- Define PostgreSQL and Redis deployment needs.
- Define secrets and configuration strategy.
- Define observability and operational concerns.

#### Review Agent

Reviews all generated artifacts.

Responsibilities:

- Check completeness.
- Check consistency across sections.
- Identify scalability, reliability, security, and maintainability risks.
- Produce required revisions or approval.
- Emit final architecture review notes.

## 6. Shared Workflow State

The LangGraph state should be typed and append-only where practical.

Conceptual state:

```text
ArchitectureDesignState
├── task_id
├── user_prompt
├── options
├── requirement_analysis
├── domain_model
├── architecture_design
├── database_design
├── api_design
├── infrastructure_design
├── deployment_design
├── architecture_review
├── errors
├── retry_counts
└── metadata
```

State rules:

- Each agent reads previous sections and writes one section.
- Agents should not mutate unrelated sections.
- Errors are captured in state for observability.
- Retry metadata is preserved.
- Final state is persisted as an architecture package.

## 7. Backend Directory Tree

```text
.
├── docs/
│   ├── architecture.md
│   └── development-plan.md
├── src/
│   └── backend_architect_agent/
│       ├── __init__.py
│       ├── main.py
│       ├── bootstrap/
│       │   ├── __init__.py
│       │   └── container.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── logging.py
│       │   └── settings.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── shared/
│       │   │   ├── __init__.py
│       │   │   ├── entity.py
│       │   │   ├── value_object.py
│       │   │   └── domain_event.py
│       │   └── architecture/
│       │       ├── __init__.py
│       │       ├── entities.py
│       │       ├── value_objects.py
│       │       ├── services.py
│       │       ├── events.py
│       │       └── exceptions.py
│       ├── application/
│       │   ├── __init__.py
│       │   ├── dto/
│       │   │   ├── __init__.py
│       │   │   └── design_task.py
│       │   ├── ports/
│       │   │   ├── __init__.py
│       │   │   ├── llm_gateway.py
│       │   │   ├── task_repository.py
│       │   │   ├── artifact_repository.py
│       │   │   ├── cache.py
│       │   │   └── unit_of_work.py
│       │   └── use_cases/
│       │       ├── __init__.py
│       │       ├── submit_design_task.py
│       │       ├── get_design_task.py
│       │       └── get_design_result.py
│       ├── presentation/
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── dependencies.py
│       │   ├── exception_handlers.py
│       │   └── api/
│       │       ├── __init__.py
│       │       ├── router.py
│       │       └── v1/
│       │           ├── __init__.py
│       │           ├── endpoints/
│       │           │   ├── __init__.py
│       │           │   └── design_tasks.py
│       │           └── schemas/
│       │               ├── __init__.py
│       │               └── design_tasks.py
│       └── infrastructure/
│           ├── __init__.py
│           ├── llm/
│           │   ├── __init__.py
│           │   ├── openai_compatible_gateway.py
│           │   └── structured_outputs.py
│           ├── langgraph/
│           │   ├── __init__.py
│           │   ├── graph.py
│           │   ├── state.py
│           │   ├── prompts/
│           │   │   ├── requirement.md
│           │   │   ├── domain.md
│           │   │   ├── architecture.md
│           │   │   ├── database.md
│           │   │   ├── api.md
│           │   │   ├── infrastructure.md
│           │   │   └── review.md
│           │   └── nodes/
│           │       ├── __init__.py
│           │       ├── requirement_node.py
│           │       ├── domain_node.py
│           │       ├── architecture_node.py
│           │       ├── database_node.py
│           │       ├── api_node.py
│           │       ├── infrastructure_node.py
│           │       └── review_node.py
│           ├── persistence/
│           │   ├── __init__.py
│           │   ├── database.py
│           │   ├── models/
│           │   │   ├── __init__.py
│           │   │   ├── design_task.py
│           │   │   └── architecture_artifact.py
│           │   └── repositories/
│           │       ├── __init__.py
│           │       ├── sqlalchemy_task_repository.py
│           │       └── sqlalchemy_artifact_repository.py
│           └── cache/
│               ├── __init__.py
│               └── redis_cache.py
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   ├── tailwind.config.ts
│   └── next.config.ts
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── langgraph/
│   ├── integration/
│   │   ├── api/
│   │   ├── persistence/
│   │   ├── cache/
│   │   └── llm/
│   └── e2e/
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── scripts/
│   ├── dev.sh
│   ├── test.sh
│   └── migrate.sh
├── pyproject.toml
└── README.md
```

## 8. Module Responsibilities

### `main.py`

Application entrypoint for ASGI servers.

Responsibilities:

- Create the FastAPI app through the application factory.
- Expose `app` for Uvicorn/Gunicorn.
- Avoid dependency construction outside bootstrap code.

### `bootstrap/`

Composition root.

Responsibilities:

- Build application settings.
- Configure logging.
- Create database engine/session factory.
- Create Redis client.
- Create LLM gateway.
- Create repositories and unit of work.
- Create application use cases.
- Wire FastAPI dependencies.

### `config/`

Configuration and runtime settings.

Responsibilities:

- Load environment variables.
- Validate settings with Pydantic v2.
- Define provider-specific LLM configuration.
- Define PostgreSQL and Redis configuration.
- Define logging configuration.

### `domain/`

Business model and DDD core.

Responsibilities:

- Define entities, value objects, aggregate roots, domain events, domain services, and exceptions.
- Enforce invariants.
- Remain independent of frameworks and infrastructure.

### `application/`

Use-case orchestration.

Responsibilities:

- Define commands, queries, DTOs, and use cases.
- Coordinate domain behavior and infrastructure ports.
- Manage transaction boundaries through unit-of-work ports.
- Start architecture generation workflows.
- Read task status and results.

### `application/ports/`

Abstract interfaces required by application use cases.

Responsibilities:

- `LLMGateway`: provider-neutral LLM access.
- `TaskRepository`: design task persistence.
- `ArtifactRepository`: generated artifact persistence.
- `Cache`: Redis-backed cache abstraction.
- `UnitOfWork`: transaction abstraction.

### `presentation/`

HTTP boundary.

Responsibilities:

- Create FastAPI app.
- Define routes and OpenAPI schemas.
- Validate requests and responses.
- Map application exceptions to HTTP responses.
- Avoid business logic.

### `infrastructure/llm/`

LLM provider implementations.

Responsibilities:

- Implement OpenAI-compatible API access.
- Support OpenAI, Qwen, DeepSeek, and custom compatible providers.
- Handle provider timeouts, retries, and structured output parsing.
- Convert provider responses into application DTOs.

### `infrastructure/langgraph/`

Agent workflow implementation.

Responsibilities:

- Define graph state.
- Define graph nodes for each agent.
- Define prompts and structured output schemas.
- Configure retry policies and error handling.
- Execute the workflow asynchronously.

### `infrastructure/persistence/`

PostgreSQL integration.

Responsibilities:

- Define SQLAlchemy async engine/session.
- Define ORM models.
- Implement repositories.
- Support Alembic migrations.

### `infrastructure/cache/`

Redis integration.

Responsibilities:

- Implement cache port.
- Store transient task state and idempotency keys.
- Support rate limiting and workflow coordination if needed.

### `frontend/`

Next.js user interface.

Responsibilities:

- Provide prompt submission UI.
- Show task progress.
- Render generated architecture sections.
- Support export/copy workflows.

## 9. API Design

Initial API surface:

```text
POST /design
GET  /tasks/{id}
GET  /tasks/{id}/result
```

### `POST /design`

Submits a backend design request.

Request:

```json
{
  "description": "Design a food delivery platform.",
  "options": {
    "target_scale": "medium",
    "deployment_target": "kubernetes",
    "include_diagrams": true
  }
}
```

Response:

```json
{
  "task_id": "uuid",
  "status": "queued"
}
```

### `GET /tasks/{id}`

Returns task status.

Response:

```json
{
  "task_id": "uuid",
  "status": "running",
  "current_step": "database_agent",
  "created_at": "2026-06-28T00:00:00Z",
  "updated_at": "2026-06-28T00:01:00Z"
}
```

### `GET /tasks/{id}/result`

Returns the final architecture package when complete.

Response:

```json
{
  "task_id": "uuid",
  "status": "completed",
  "result": {
    "requirement_analysis": {},
    "domain_model": {},
    "service_decomposition": {},
    "database_design": {},
    "api_design": {},
    "infrastructure_design": {},
    "deployment_design": {},
    "architecture_review": {}
  }
}
```

## 10. Persistence Design

Primary tables:

### `design_tasks`

Stores task lifecycle.

Fields:

- `id`
- `input_description`
- `status`
- `current_step`
- `error_message`
- `created_at`
- `updated_at`
- `completed_at`

### `architecture_artifacts`

Stores generated architecture sections.

Fields:

- `id`
- `task_id`
- `artifact_type`
- `content_json`
- `version`
- `created_at`
- `updated_at`

### `workflow_events`

Stores workflow observability events.

Fields:

- `id`
- `task_id`
- `step_name`
- `event_type`
- `payload_json`
- `created_at`

## 11. Redis Usage

Redis should be used for:

- Task status cache.
- Idempotency keys for repeated submissions.
- Rate limiting counters.
- Temporary workflow state if durable persistence is not required at every step.
- Distributed locks if multiple workers process graph tasks.

PostgreSQL remains the durable source of truth.

## 12. Error Handling Strategy

Error categories:

- Validation errors.
- Task not found.
- Task not ready.
- LLM provider errors.
- Workflow node errors.
- Persistence errors.
- Unexpected internal errors.

Strategy:

- Domain raises domain-specific exceptions.
- Application translates infrastructure failures into use-case errors.
- Presentation maps use-case errors to HTTP status codes.
- Workflow state records recoverable errors.
- Failed tasks persist error details for retrieval.

## 13. Observability

Minimum production observability:

- Structured JSON logs.
- Request IDs.
- Task IDs in all workflow logs.
- LLM provider latency metrics.
- Workflow step duration metrics.
- Database query timing.
- Redis operation timing.
- Error counters by category.

## 14. Security

Security requirements:

- Store API keys in environment variables or secret manager.
- Never log raw API keys.
- Validate user input length and content.
- Apply rate limits to design submissions.
- Use authentication before exposing user-owned tasks in production.
- Scope task result access by authenticated user or tenant.
- Sanitize generated markdown before frontend rendering.

## 15. Deployment Architecture

Production topology:

```text
Browser
  ↓
Next.js Frontend
  ↓
FastAPI Backend
  ↓
PostgreSQL
  ↓
Redis

FastAPI Backend
  ↓
LangGraph Worker / In-process Workflow
  ↓
OpenAI-compatible LLM Provider
```

Initial deployment can run workflow execution in-process. As volume grows, move workflow execution to background workers backed by PostgreSQL/Redis coordination.

## 16. Implementation Boundaries for This Phase

This architecture phase intentionally does not implement new business logic.

Allowed in this phase:

- Architecture documentation.
- Development plan.
- Directory tree proposal.
- Module responsibility definitions.

Deferred:

- New FastAPI routes.
- LangGraph node implementation.
- SQLAlchemy models.
- Alembic migrations.
- Redis clients.
- LLM prompts.
- Frontend code.
