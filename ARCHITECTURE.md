# ARCHITECTURE — Assignment Service

**Proyecto:** backend-assignment-service  
**Servicio:** assignment-service (microservicio Django DDD + EDA)  
**Fecha:** 2026-02-26  
**Equipo:** Equipo 6 Uruguay  
**Referencia conceptual:** *Clean Architecture* — Robert C. Martin (Uncle Bob)

---

## 1. Introducción

`assignment-service` es el microservicio responsable de gestionar la asignación de tickets, su prioridad y su responsable operativo dentro del ecosistema de microservicios. En este contexto, actúa como frontera entre:

- el canal síncrono HTTP (API REST para clientes internos), y
- el canal asíncrono de eventos (RabbitMQ + Celery) para integración con `ticket-service`.

La solución está implementada sobre **Django 6.0.2 + DRF 3.16.1**, con persistencia en **PostgreSQL** y mensajería en **RabbitMQ**, siguiendo un enfoque de **Domain-Driven Design (DDD)** y **Event-Driven Architecture (EDA)**.

---

## 2. Debate Arquitectónico: Monolito vs Clean Architecture

Este documento consolida el debate formal iniciado en [Actividad_1.1.md](Actividad_1.1.md), donde se identifican 24 dolores técnicos del código heredado y se evalúa su remediación con principios de Clean Architecture + SOLID.

### 2.1 ¿Qué es Clean Architecture?

Clean Architecture organiza el sistema en capas concéntricas donde las reglas de negocio están en el centro (dominio y casos de uso), y los detalles tecnológicos (framework, DB, broker, transporte) quedan en la periferia.

Regla principal:

> Las dependencias del código deben apuntar hacia adentro (Dependency Rule).

Esto habilita independencia de framework, testabilidad de reglas de negocio y menor costo de cambio tecnológico.

### 2.2 Tabla comparativa: dolores vs principios CA/SOLID vs beneficio

| Dolor | Principio(s) CA / SOLID | Beneficio esperado |
|---|---|---|
| CPL-01 ViewSet instancia repositorio/publisher concretos | Dependency Rule + DIP + SRP | Desacoplar controlador de infraestructura; tests de aplicación sin framework |
| CPL-02 Handler crea dependencias concretas por evento | DIP + SRP + OCP | Composición centralizada y menor acoplamiento por evento |
| DUP-01 Integración duplicada en dos archivos | SRP + OCP | Menos divergencia y menor costo de mantenimiento |
| ERR-01 `save()` update sin manejar `DoesNotExist` | SRP + DIP | Errores explícitos de dominio en lugar de 500 opacos |
| ERR-02 `except Exception` genérico | SRP + ISP | Diagnóstico y recuperación más precisa |
| ERR-03 Reconexión captura todo error | SRP + OCP | Retry selectivo para fallos transitorios |
| MOD-01 God test file mezclando capas | SRP | Suite modular por contexto (dominio/app/infra/API) |
| CFG-01 Credenciales RabbitMQ hardcodeadas | DIP + 12-Factor | Seguridad y portabilidad por entorno |
| CFG-02 CMD mezcla migración + worker | SRP | Operación desacoplada por proceso |
| TST-01 Tests replican internals del consumer | OCP + testabilidad por comportamiento | Menos falsos positivos |
| TST-02 URLs de tests no coinciden con router real | SRP | Coherencia entre contrato API y pruebas |
| SCL-01 Sin paginación global | OCP + SRP | Performance estable con datasets grandes |
| SCL-02 Nueva conexión RabbitMQ por evento | SRP + OCP | Menor latencia y mayor throughput |
| SLD-01 `event_publisher` inyectado pero no usado | ISP + SRP | Contratos más claros y menos deuda cognitiva |
| SLD-02 Dominio usa `ValueError` genérico | SRP + lenguaje ubicuo | Errores de negocio semánticos |
| NOM-01 Docstring con término incorrecto | SRP | Mejor claridad de mantenimiento |
| NOM-02 Import muerto (`random`) | SRP | Código más limpio y menos ruido |
| DOC-01 Serializer sin validadores explícitos | SRP en borde de entrada | Contrato HTTP más explícito |
| SEC-01 `ALLOWED_HOSTS` vacío con `DEBUG=False` | Security by default | Menor exposición en producción |
| SEC-02 Fallback CSRF permisivo | Configuración por entorno + SRP | Menor riesgo de configuración insegura |
| EDA-01 ACK prematuro antes de procesar | Boundary Control + SRP | Evita pérdida silenciosa de mensajes |
| EDA-02 Celery sin retry/backoff | OCP + SRP | Mayor resiliencia ante fallos transitorios |
| EDA-03 Inconsistencia de routing key DLQ | Contrato explícito entre adapters | Menos incidentes operativos |
| DEB-01 Divergencia migración/modelo | Single Source of Truth + SRP | Despliegues más predecibles |

### 2.3 Argumentación clave: independencia de framework, UI y BD

La decisión de evolucionar desde un monolito acoplado a infraestructura hacia Clean Architecture se sostiene en tres ejes:

- **Independencia de framework:** Django/DRF deben ser mecanismos de entrega, no núcleo de negocio.
- **Independencia de interfaz:** la misma regla de negocio debe operar igual desde HTTP, tareas async o eventos.
- **Independencia de base de datos:** PostgreSQL/ORM son detalles reemplazables detrás de puertos.

Resultado esperado: cambios más localizados, menor riesgo de regresiones transversales y mayor velocidad de evolución del microservicio.

---

## 3. Arquitectura del Sistema

### 3.1 Diagrama de capas (ASCII)

```text
┌────────────────────────────────────────────────────────────────────┐
│                     Frameworks & Drivers                          │
│ Django, DRF, ORM, RabbitMQ, Celery, Docker, Settings, JWT        │
└───────────────────────────────▲────────────────────────────────────┘
                                │ implementa puertos
┌───────────────────────────────┴────────────────────────────────────┐
│                      Interface Adapters                            │
│ ViewSet, Serializers, DjangoAssignmentRepository, Event Adapter   │
└───────────────────────────────▲────────────────────────────────────┘
                                │ orquesta casos de uso
┌───────────────────────────────┴────────────────────────────────────┐
│                     Application / Use Cases                        │
│ CreateAssignment, ReassignTicket, ChangeAssignmentPriority,       │
│ UpdateAssignedUser + puertos (Repository, EventPublisher)         │
└───────────────────────────────▲────────────────────────────────────┘
                                │ reglas de negocio puras
┌───────────────────────────────┴────────────────────────────────────┐
│                         Entities / Domain                          │
│ Assignment, Domain Events, Domain invariants                      │
└────────────────────────────────────────────────────────────────────┘
```

### 3.2 Mapeo de componentes actuales a capas

| Capa | Componentes |
|---|---|
| Entities / Domain | `assignments/domain/entities.py`, `assignments/domain/events.py`, `assignments/domain/repository.py` |
| Application / Use Cases | `assignments/application/use_cases/*`, `assignments/application/event_publisher.py` |
| Interface Adapters | `assignments/views.py`, `assignments/serializers.py`, `assignments/infrastructure/repository.py`, `assignments/infrastructure/messaging/event_adapter.py` |
| Frameworks & Drivers | `assessment_service/settings.py`, `assessment_service/urls.py`, `assignments/infrastructure/django_models.py`, `messaging/consumer.py`, `assignments/tasks.py` |

### 3.3 Flujo de datos HTTP

1. Cliente invoca endpoint REST (`/api/assignments/...`) con JWT.
2. `TicketAssignmentViewSet` valida body mediante serializer DRF.
3. ViewSet delega en caso de uso (`CreateAssignment`, `ReassignTicket`, etc.).
4. Caso de uso aplica reglas de dominio y persiste vía `AssignmentRepository`.
5. Repositorio concreto usa ORM Django sobre PostgreSQL.
6. Caso de uso publica evento de dominio (RabbitMQ) cuando corresponde.
7. API retorna respuesta JSON y código HTTP.

### 3.4 Flujo de eventos EDA

1. RabbitMQ recibe `ticket.created` / `ticket.priority_changed` desde ticket-service.
2. Consumer entrega payload a Celery (`process_ticket_event`).
3. Handler (`messaging/handlers.py`) usa `TicketEventAdapter`.
4. Adapter traduce evento externo a caso de uso de aplicación.
5. Caso de uso persiste en DB y emite evento saliente (`assignment.created` / `assignment.reassigned`).
6. Publisher publica en exchange de RabbitMQ.
7. Fallas no recuperables se enrutan a DLQ según política de mensajería.

---

## 4. Contrato de API REST

### 4.1 Base URL y autenticación

- **Prefijo base:** `/api/`
- **Resource base:** `/api/assignments/`
- **Auth:** JWT Bearer (`Authorization: Bearer <token>`)
- **Permisos por defecto:** `IsAuthenticated`
- **Content-Type:** `application/json`

### 4.2 Modelo de datos (Assignment)

| Campo | Tipo | Requerido | Nullable | Solo lectura | Regla |
|---|---|---|---|---|---|
| `id` | integer | No (auto) | No | Sí | PK autogenerada |
| `ticket_id` | string | Sí | No | No | Único por asignación |
| `priority` | string | Sí | No | No | `high`, `medium`, `low`, `unassigned` |
| `assigned_at` | datetime ISO-8601 | No (auto) | No | Sí | Fecha/hora de asignación |
| `assigned_to` | string | No | Sí | No | Usuario asignado o `null` |

### 4.3 Tabla de endpoints

| Verbo | Ruta | Descripción | Body request | Códigos |
|---|---|---|---|---|
| POST | `/api/assignments/` | Crea asignación (idempotente por `ticket_id`) | `ticket_id`, `priority`, `assigned_to?` | `201`, `400` |
| GET | `/api/assignments/` | Lista asignaciones (orden desc por `assigned_at`) | — | `200` |
| GET | `/api/assignments/{id}/` | Obtiene asignación por ID | — | `200`, `404` |
| PUT | `/api/assignments/{id}/` | Reemplazo completo de asignación | `ticket_id`, `priority`, `assigned_to?` | `200`, `400`, `404` |
| PATCH | `/api/assignments/{id}/` | Actualización parcial | campos parciales | `200`, `400`, `404` |
| DELETE | `/api/assignments/{id}/` | Elimina asignación | — | `204`, `404` |
| POST | `/api/assignments/reassign/` | Reasigna prioridad por `ticket_id` | `ticket_id`, `priority` | `200`, `400` |
| PATCH | `/api/assignments/{id}/assign-user/` | Asigna/reasigna/desasigna usuario | `assigned_to` (string o `null`) | `200`, `400` |

### 4.4 Detalle de endpoints (request/response)

#### 4.4.1 POST `/api/assignments/`

Crea una asignación. Si el `ticket_id` ya existe, la operación es idempotente y retorna la asignación existente.

**Request**
```http
POST /api/assignments/
Authorization: Bearer <jwt>
Content-Type: application/json
```

```json
{
  "ticket_id": "TK-100",
  "priority": "high",
  "assigned_to": "agent-1"
}
```

**Response 201 Created**
```json
{
  "id": 1,
  "ticket_id": "TK-100",
  "priority": "high",
  "assigned_at": "2026-02-26T14:10:33.221000Z",
  "assigned_to": "agent-1"
}
```

**Response 400 Bad Request (ejemplo)**
```json
{
  "error": "priority debe ser uno de {'high', 'medium', 'low', 'unassigned'}"
}
```

#### 4.4.2 GET `/api/assignments/`

Lista todas las asignaciones ordenadas por `assigned_at` descendente.

**Request**
```http
GET /api/assignments/
Authorization: Bearer <jwt>
```

**Response 200 OK**
```json
[
  {
    "id": 3,
    "ticket_id": "TK-300",
    "priority": "medium",
    "assigned_at": "2026-02-26T15:05:11.000000Z",
    "assigned_to": null
  },
  {
    "id": 1,
    "ticket_id": "TK-100",
    "priority": "high",
    "assigned_at": "2026-02-26T14:10:33.221000Z",
    "assigned_to": "agent-1"
  }
]
```

#### 4.4.3 GET `/api/assignments/{id}/`

Obtiene una asignación por `id`.

**Request**
```http
GET /api/assignments/1/
Authorization: Bearer <jwt>
```

**Response 200 OK**
```json
{
  "id": 1,
  "ticket_id": "TK-100",
  "priority": "high",
  "assigned_at": "2026-02-26T14:10:33.221000Z",
  "assigned_to": "agent-1"
}
```

**Response 404 Not Found**
```json
{
  "detail": "No TicketAssignment matches the given query."
}
```

#### 4.4.4 PUT `/api/assignments/{id}/`

Actualiza completamente una asignación existente.

**Request**
```http
PUT /api/assignments/1/
Authorization: Bearer <jwt>
Content-Type: application/json
```

```json
{
  "ticket_id": "TK-100",
  "priority": "medium",
  "assigned_to": "agent-2"
}
```

**Response 200 OK**
```json
{
  "id": 1,
  "ticket_id": "TK-100",
  "priority": "medium",
  "assigned_at": "2026-02-26T14:10:33.221000Z",
  "assigned_to": "agent-2"
}
```

**Response 400 Bad Request (ejemplo)**
```json
{
  "priority": [
    "Este campo es requerido."
  ]
}
```

**Response 404 Not Found**
```json
{
  "detail": "No TicketAssignment matches the given query."
}
```

#### 4.4.5 PATCH `/api/assignments/{id}/`

Actualiza parcialmente una asignación.

**Request**
```http
PATCH /api/assignments/1/
Authorization: Bearer <jwt>
Content-Type: application/json
```

```json
{
  "priority": "low"
}
```

**Response 200 OK**
```json
{
  "id": 1,
  "ticket_id": "TK-100",
  "priority": "low",
  "assigned_at": "2026-02-26T14:10:33.221000Z",
  "assigned_to": "agent-2"
}
```

**Response 400 / 404** según validación o inexistencia del recurso.

#### 4.4.6 DELETE `/api/assignments/{id}/`

Elimina una asignación por ID.

**Request**
```http
DELETE /api/assignments/1/
Authorization: Bearer <jwt>
```

**Response 204 No Content**
```text
(sin cuerpo)
```

**Response 404 Not Found**
```json
{
  "detail": "No TicketAssignment matches the given query."
}
```

#### 4.4.7 POST `/api/assignments/reassign/`

Cambia prioridad por `ticket_id` usando caso de uso de reasignación.

**Request**
```http
POST /api/assignments/reassign/
Authorization: Bearer <jwt>
Content-Type: application/json
```

```json
{
  "ticket_id": "TK-300",
  "priority": "high"
}
```

**Response 200 OK**
```json
{
  "id": 3,
  "ticket_id": "TK-300",
  "priority": "high",
  "assigned_at": "2026-02-26T15:05:11.000000Z",
  "assigned_to": null
}
```

**Response 400 Bad Request (ejemplo)**
```json
{
  "error": "No se encontró una asignación para el ticket TK-300"
}
```

#### 4.4.8 PATCH `/api/assignments/{id}/assign-user/`

Asigna, reasigna o desasigna (`null`) el usuario responsable de una asignación.

**Request (asignar/reasignar)**
```http
PATCH /api/assignments/3/assign-user/
Authorization: Bearer <jwt>
Content-Type: application/json
```

```json
{
  "assigned_to": "agent-15"
}
```

**Request (desasignar)**
```json
{
  "assigned_to": null
}
```

**Response 200 OK**
```json
{
  "id": 3,
  "ticket_id": "TK-300",
  "priority": "high",
  "assigned_at": "2026-02-26T15:05:11.000000Z",
  "assigned_to": "agent-15"
}
```

**Response 400 Bad Request (ejemplo)**
```json
{
  "error": "No existe una asignación con id 999"
}
```

### 4.5 Códigos de respuesta

| Código | Significado | Cuándo ocurre |
|---|---|---|
| `200 OK` | Operación exitosa | GET, PUT, PATCH, reassign, assign-user |
| `201 Created` | Recurso creado | POST create |
| `204 No Content` | Eliminación exitosa | DELETE |
| `400 Bad Request` | Error de validación o regla de negocio | prioridad inválida, body inválido, ticket/assignment inexistente en casos de uso custom |
| `401 Unauthorized` | JWT ausente o inválido | petición sin credenciales válidas |
| `403 Forbidden` | Sin permisos para recurso | política de permisos del API |
| `404 Not Found` | Recurso no encontrado | GET/PUT/PATCH/DELETE por `id` inexistente |

---

## 5. Contrato de Eventos

### 5.1 Eventos consumidos

#### 5.1.1 `ticket.created`

Evento proveniente de `ticket-service`, consumido por `assignment-service` para crear asignación inicial.

**Payload esperado (ejemplo):**
```json
{
  "event_type": "ticket.created",
  "ticket_id": "TK-500",
  "priority": "unassigned",
  "occurred_at": "2026-02-26T15:40:00Z"
}
```

Reglas:
- Si falta `ticket_id`, el evento se ignora.
- Si no llega `priority`, se usa `unassigned` por defecto.

#### 5.1.2 `ticket.priority_changed`

Evento consumido para sincronizar cambio de prioridad en asignación existente.

**Payload esperado (ejemplo):**
```json
{
  "event_type": "ticket.priority_changed",
  "ticket_id": "TK-500",
  "new_priority": "high",
  "occurred_at": "2026-02-26T15:42:00Z"
}
```

Reglas:
- Requiere `ticket_id` y `new_priority`.
- Si no existe asignación asociada, se registra el caso y no se publica evento de salida.

### 5.2 Eventos publicados

#### 5.2.1 `assignment.created`

Emitido al crear una asignación.

**Schema (ejemplo):**
```json
{
  "event_type": "assignment.created",
  "assignment_id": 10,
  "ticket_id": "TK-500",
  "priority": "high",
  "assigned_to": "agent-7",
  "occurred_at": "2026-02-26T15:45:10.111111"
}
```

#### 5.2.2 `assignment.reassigned`

Emitido al cambiar prioridad de una asignación.

**Schema (ejemplo):**
```json
{
  "event_type": "assignment.reassigned",
  "assignment_id": 10,
  "ticket_id": "TK-500",
  "old_priority": "medium",
  "new_priority": "high",
  "occurred_at": "2026-02-26T15:49:00.999999"
}
```

---

## 6. Propuesta de Mejora (Pseudocódigo CA)

Resumen de los 6 dolores críticos documentados en [Actividad_1.1.md](Actividad_1.1.md):

### 6.1 CPL-01 — ViewSet desacoplado por Composition Root + DIP

**Antes (acoplado):**
```python
class TicketAssignmentViewSet(ModelViewSet):
    def __init__(...):
        self.repository = DjangoAssignmentRepository()
        self.event_publisher = RabbitMQEventPublisher()
```

**Después (CA):**
```python
container = build_assignment_container()
viewset = TicketAssignmentViewSet(container=container)
```

### 6.2 ERR-01 — Excepciones por frontera

**Antes:**
```python
model = TicketAssignmentModel.objects.get(id=assignment.id)
```

**Después:**
```python
try:
    model = TicketAssignmentModel.objects.get(id=assignment.id)
except TicketAssignmentModel.DoesNotExist:
    raise AssignmentNotFound(...)
```

### 6.3 EDA-01 — ACK luego de procesar

**Antes:**
```python
process_ticket_event.delay(event)
ch.basic_ack(...)
```

**Después:**
```python
result = processor.process(event)
if result.success:
    ch.basic_ack(...)
else:
    ch.basic_nack(...)
```

### 6.4 CFG-01 — Credenciales por variables de entorno

**Antes:**
```python
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
```

**Después:**
```python
CELERY_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
```

### 6.5 SCL-01 — Paginación global

**Antes:**
```python
REST_FRAMEWORK = {...}
```

**Después:**
```python
REST_FRAMEWORK = {
  ...,
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 20,
}
```

### 6.6 SLD-02 — Excepciones de dominio semánticas

**Antes:**
```python
raise ValueError("priority inválida")
```

**Después:**
```python
raise InvalidPriority("...")
```

---

## 7. Conclusión

El análisis confirma que el servicio ya tiene base DDD/EDA, pero aún convive con acoplamientos de infraestructura y brechas operativas. La adopción explícita de Clean Architecture permite convertir ese diseño en una arquitectura robusta, testeable y evolutiva.

Como resultado, este documento deja definidos:

1. un marco de decisión arquitectónico (monolito heredado vs Clean Architecture), y
2. un **contrato API REST formal** y consumible para integración entre equipos.

Esto habilita una hoja de ruta técnica coherente con los entregables del taller: calidad de diseño, claridad contractual y reducción de deuda técnica estructural.

---

## Referencias cruzadas

- [Actividad_1.1.md](Actividad_1.1.md)
- [TEST_PLAN_V3.md](TEST_PLAN_V3.md)
- [USERSTORIES Y CRITERIOS DE ACEPTACION.md](USERSTORIES%20Y%20CRITERIOS%20DE%20ACEPTACION.md)