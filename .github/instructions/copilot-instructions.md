# Copilot Instructions — Assignment Service

## Architecture Overview

This is a **Django-based assignment service** using **DDD + EDA**.

### Core principle

- Domain model lives in `assignments/domain/` and must stay framework-agnostic.
- ORM model lives in `assignments/infrastructure/django_models.py` and is persistence-only.
- Use cases orchestrate domain behavior and depend on interfaces, not concrete infra.

## Layer map (real repo)

### Domain (`assignments/domain/`)
- `entities.py`: `Assignment` entity + invariants (`ticket_id`, valid priorities)
- `events.py`: domain events (`AssignmentCreated`, `AssignmentReassigned`)
- `repository.py`: `AssignmentRepository` interface

### Application (`assignments/application/`)
- `use_cases/`: create/reassign/change priority/update assigned user
- `event_publisher.py`: application-level publisher interface

### Infrastructure (`assignments/infrastructure/`)
- `repository.py`: `DjangoAssignmentRepository`
- `django_models.py`: persistence model
- `messaging/event_publisher.py`: RabbitMQ adapter
- `messaging/event_adapter.py`: external ticket event adapter

### Delivery / integration
- HTTP API: `assignments/views.py`, `assignments/serializers.py`, `assignments/urls.py`
- Async consumer: `messaging/consumer.py`, `messaging/handlers.py`
- Celery task entrypoint: `assignments/tasks.py`

## API and routing

- Base API prefix is `/api/`.
- Assignment routes are mounted under `/api/assignments/`.

## Testing conventions

- Prefer `pytest`.
- When testing `handle_ticket_event()`, patch publisher at lookup site:
  - `@patch('messaging.handlers.RabbitMQEventPublisher')`
- API tests usually need auth override (`AllowAny`) unless validating auth behavior.
- Avoid duplicating integration scenarios across multiple files.

## Reliability conventions

- Avoid generic `except Exception` unless re-raising with clear context.
- Keep retry/backoff behavior explicit in async paths.
- Keep DLQ naming/routing consistent between implementation and tests.

## Documentation conventions

- Keep these docs aligned with runtime code and merged PR state:
  - `DOLORES.md`
  - `DOLORES_RESUELTOS.md`
  - `ARCHITECTURE.md`
  - `GHERKIN_MATRIX.md`
  - `TEST_PLAN_V3.md`
  - `USERSTORIES Y CRITERIOS DE ACEPTACION.md`
- Do not mark a pain as resolved unless merged into target branch.
