# backend-assignment-service

Servicio de asignaciones construido con Django + DRF, aplicando DDD + EDA.

## Objetivo

Gestionar asignaciones de tickets, prioridad y responsable operativo, con integracion HTTP y mensajeria (RabbitMQ/Celery).

## Stack

- Python
- Django 6.0.2
- Django REST Framework
- PostgreSQL
- RabbitMQ
- Celery
- Docker Compose

## Estructura principal

- `assignments/domain/`: entidades, eventos y contratos de dominio.
- `assignments/application/`: casos de uso y puertos de aplicacion.
- `assignments/infrastructure/`: repositorio Django y adaptadores de mensajeria.
- `assignments/views.py`: capa de entrega HTTP.
- `messaging/`: consumo de eventos externos.

## Ejecucion local (Docker)

```bash
docker compose up -d --build
```

## Tests

Suite principal de assignments:

```bash
docker compose exec backend pytest assignments/tests -q
```

Suite Django del servicio:

```bash
docker compose exec backend python manage.py test assignments messaging --verbosity=2
```

## Endpoints base

- Base API: `/api/`
- Assignments: `/api/assignments/`

## Documentacion relevante

- `ARCHITECTURE.md`
- `DOLORES.md`
- `DOLORES_RESUELTOS.md`
- `TEST_PLAN_V3.md`
- `GHERKIN_MATRIX.md`
- `USERSTORIES Y CRITERIOS DE ACEPTACION.md`
