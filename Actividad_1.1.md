# Debate Arquitectónico: Dolores vs Clean Architecture

**Proyecto:** Assignment Service (Django + DDD + EDA)  
**Fecha:** 24 de Febrero, 2026  
**Versión:** 1.0  
**Equipo:** Equipo 6 Uruguay  
**Referencia:** Clean Architecture — Robert C. Martin (Uncle Bob)

---

## 1. Introducción

El monolito **Assignment Service** (Django + DDD + EDA) ya muestra intenciones de separación por capas, pero todavía conserva acoplamientos fuertes a framework, infraestructura y configuración operativa que frenan su evolución. Se identificaron **18+ hallazgos** distribuidos en 13 categorías de deuda técnica.

El objetivo de esta actividad es formalizar el **debate arquitectónico**: contrastar teóricamente los "dolores" del proyecto heredado con los beneficios que aportaría migrar hacia una **Clean Architecture** explícita, siguiendo a **Robert C. Martin (Uncle Bob)**.

### ¿Qué es Clean Architecture?

Clean Architecture organiza el software en capas concéntricas donde las **reglas de negocio** ocupan el centro y los **detalles técnicos** (framework, base de datos, mensajería, UI) se ubican en la periferia. La regla fundamental es la **Dependency Rule**:

> *"Las dependencias del código fuente deben apuntar siempre hacia adentro, hacia las políticas de nivel superior."*  
> — Robert C. Martin, *Clean Architecture* (2017)

Esto significa que las entidades de dominio **nunca** importan Django, RabbitMQ o PostgreSQL. Los casos de uso **nunca** conocen el framework HTTP. Y los adaptadores de infraestructura **implementan** interfaces definidas por las capas internas — no al revés.

---

## 2. Análisis Comparativo

La siguiente tabla mapea **cada dolor** identificado con el principio de Clean Architecture / SOLID que lo resuelve y el beneficio concreto esperado tras la migración.

| Dolor | Principio(s) Clean Architecture / SOLID | Beneficio Concreto Esperado |
|---|---|---|
| **CPL-01** ViewSet instancia repositorio/publisher concretos | Dependency Rule + **DIP** + SRP | Cambiar Django/RabbitMQ sin tocar casos de uso; tests de aplicación sin framework |
| **CPL-02** Handler crea dependencias concretas por evento | **DIP** + SRP + OCP | Menor acoplamiento por mensaje; composición centralizada de dependencias |
| **DUP-01** Integración duplicada en dos archivos | SRP + OCP | Menos costo de mantenimiento y menor riesgo de divergencia entre suites |
| **ERR-01** `save()` update sin manejar `DoesNotExist` | SRP + manejo de errores por frontera + DIP | Fallas controladas de dominio/aplicación en vez de 500 opacos |
| **ERR-02** `except Exception` genérico en publisher/adapter | SRP + ISP (errores específicos) | Observabilidad y políticas de recuperación diferenciadas |
| **ERR-03** Reconexión captura todo error | SRP + OCP | Retry solo para fallas transitorias; errores de programación fallan rápido |
| **MOD-01** God test file mezclando capas/estilos | SRP + separación de capas | Suite legible, modular y estable por contexto (dominio/app/infra/API) |
| **CFG-01** Credenciales RabbitMQ hardcodeadas | Frameworks & Drivers como detalle + Dependency Rule + DIP | Seguridad por entorno y despliegue portable |
| **CFG-02** CMD mezcla migración + worker | SRP + separación de responsabilidades operativas | Operación escalable por proceso (web/worker/migrate) |
| **TST-01** Tests replican lógica interna del consumer | Testabilidad de casos de uso/adapters + OCP | Evita falsos positivos; valida comportamiento real del sistema |
| **TST-02** URLs de tests no coinciden con router real | Interface Adapters como contrato + SRP | Coherencia entre API pública y pruebas de aceptación |
| **SCL-01** Sin paginación global | OCP + SRP en capa de presentación | Rendimiento estable con dataset grande y menor presión de red |
| **SCL-02** Nueva conexión RabbitMQ por evento | SRP en infraestructura + OCP | Mayor throughput y menor latencia bajo carga |
| **SLD-01** Se inyecta `event_publisher` pero no se usa | **ISP** + DIP + SRP | Contratos más precisos y menor deuda cognitiva |
| **SLD-02** Dominio usa `ValueError` genérico | SRP + lenguaje ubicuo del dominio + DIP | Errores semánticos de negocio y mejor traducción a API |
| **NOM-01** Docstring con término incorrecto | SRP (claridad) + cohesión semántica | Menor ambigüedad para desarrollo y soporte |
| **NOM-02** Import muerto (`random`) | SRP + limpieza de dependencias | Menos ruido y menor riesgo de mantenimiento accidental |
| **DOC-01** Serializer sin validadores explícitos | Interface Adapters (validación en borde) + SRP | Contrato HTTP claro antes de entrar al dominio |
| **SEC-01** `ALLOWED_HOSTS` vacío con `DEBUG=False` | Fail-safe defaults + políticas explícitas separadas del framework | Menor exposición a ataques por Host header |
| **SEC-02** Fallback CSRF permisivo no condicionado por entorno | Políticas explícitas por entorno + SRP de configuración | Menor riesgo de configuración insegura en no-dev |
| **EDA-01** ACK prematuro antes de confirmar procesamiento | Boundary control en adapters + SRP + DIP | Reduce pérdida de mensajes; trazabilidad real del procesamiento |
| **EDA-02** Celery sin retry/backoff explícito | OCP + SRP (resiliencia en infraestructura) | Tolerancia a fallos transitorios y mayor confiabilidad |
| **EDA-03** Inconsistencia de routing key DLQ | Contratos explícitos entre adapters + OCP | Menos incidentes operativos por mismatch de enrutamiento |
| **DEB-01** Divergencia migración vs modelo (`assigned_at`) | Single Source of Truth de persistencia + SRP | Menos drift entre entornos y despliegues predecibles |

### 2.1 Argumentación Clave: Independencia de Framework, UI y Base de Datos

El argumento central para la migración se fundamenta en tratar **Django, DRF, RabbitMQ y PostgreSQL** como **detalles externos reemplazables**, no como pilares del diseño:

- **Independencia de Framework:** Si Django/DRF son detalles de la periferia, el núcleo (entidades + casos de uso) no se rompe al cambiar de framework. Actualmente, el ViewSet (CPL-01) conoce directamente `DjangoAssignmentRepository`, lo que viola la Dependency Rule.

- **Independencia de UI:** Los casos de uso no deberían saber si son invocados desde HTTP, CLI o un consumer de RabbitMQ. Actualmente, el handler de mensajería (CPL-02) recrea dependencias concretas por cada evento porque no existe una composición raíz centralizada.

- **Independencia de Base de Datos:** El repositorio debería implementar una interfaz definida por el dominio, no exponer detalles de ORM. Actualmente, un `DoesNotExist` de Django (ERR-01) se filtra como error 500 porque la infraestructura no traduce a excepciones de dominio.

- **Testabilidad como consecuencia:** Al mover políticas al centro, los casos de uso se ejecutan sin servidor web, sin broker y sin ORM real. El mantenimiento deja de ser "cambio transversal" y pasa a ser "cambio localizado por capa".

- **Decisiones reversibles:** Las decisiones de infraestructura se vuelven de menor costo porque afectan solo la capa externa, no las reglas de negocio.

---

## 3. Propuesta de Capas

El sistema se reestructurará siguiendo el esquema concéntrico de Clean Architecture:

### 3.1 Diagrama de Capas

```text
┌─────────────────────────────────────────────────────────────┐
│                  Frameworks & Drivers                       │
│  Django, DRF, ORM Model, RabbitMQ, Celery, Settings, Docker │
└───────────────────────▲─────────────────────────────────────┘
                        │ implementa puertos / inyección
┌───────────────────────┴─────────────────────────────────────┐
│                  Interface Adapters                          │
│  Views (Controllers), Serializers (Presenters), Repositorios │
│  Concretos, Event Adapters (Gateways)                        │
└───────────────────────▲─────────────────────────────────────┘
                        │ llama casos de uso / traduce DTOs
┌───────────────────────┴─────────────────────────────────────┐
│              Application (Use Cases)                         │
│  CreateAssignment, ReassignTicket, ChangePriority            │
│  Puertos: AssignmentRepository, EventPublisher               │
└───────────────────────▲─────────────────────────────────────┘
                        │ reglas de negocio puras
┌───────────────────────┴─────────────────────────────────────┐
│                 Entities (Domain)                             │
│  Assignment, DomainEvents, DomainExceptions                  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Mapeo de Componentes Actuales a Capas Objetivo

| Capa CA | Componentes Actuales | Qué Cambia |
|---|---|---|
| **Entities** | `assignments/domain/entities.py`, `assignments/domain/events.py` | Agregar jerarquía de `DomainException` (SLD-02) |
| **Use Cases** | `assignments/application/use_cases/*.py` | Eliminar `event_publisher` donde no se usa (SLD-01); estandarizar manejo de errores |
| **Ports (Interfaces)** | `assignments/domain/repository.py`, `assignments/application/event_publisher.py` | Sin cambios — ya existen como abstracciones |
| **Interface Adapters** | `assignments/views.py`, `assignments/serializers.py`, `assignments/infrastructure/repository.py`, `assignments/infrastructure/messaging/event_adapter.py` | ViewSet recibe dependencias inyectadas (CPL-01); Repository maneja `DoesNotExist` (ERR-01); Serializer agrega validadores (DOC-01) |
| **Frameworks & Drivers** | `assessment_service/settings.py`, `assignments/infrastructure/django_models.py`, `messaging/consumer.py`, `assignments/tasks.py`, `Dockerfile` | Externalizar credenciales (CFG-01); separar entrypoints (CFG-02); paginación global (SCL-01); ACK post-procesamiento (EDA-01); retry en tasks (EDA-02) |

---

## 4. Pseudocódigo de Solución — 6 Dolores Críticos

Para cada dolor de severidad alta, se muestra el **estado actual** (código real del monolito) contrastado con el **estado propuesto** siguiendo Clean Architecture.

---

### 4.1 [CPL-01] Desacoplamiento de ViewSet — Dependency Inversion

**Estado Actual** (monolito):
Fuente: `assignments/views.py` (líneas 8-34)

```python
from .infrastructure.repository import DjangoAssignmentRepository
from .infrastructure.messaging.event_publisher import RabbitMQEventPublisher

class TicketAssignmentViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = DjangoAssignmentRepository()        # ← Concreto
        self.event_publisher = RabbitMQEventPublisher()        # ← Concreto

    def create(self, request, *args, **kwargs):
        use_case = CreateAssignment(self.repository, self.event_publisher)
        # ...
```

**Estado Propuesto** (Clean Architecture):

```python
# === Composition Root (Frameworks & Drivers) ===
# assessment_service/container.py
def build_assignment_container() -> AssignmentContainer:
    repo = DjangoAssignmentRepository()
    publisher = RabbitMQEventPublisher()
    return AssignmentContainer(
        create_assignment=CreateAssignment(repo, publisher),
        reassign_ticket=ReassignTicket(repo, publisher),
        update_assigned_user=UpdateAssignedUser(repo, publisher),
    )

# === Interface Adapter (View) ===
# assignments/views.py
class TicketAssignmentViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, container=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container or get_assignment_container()

    def create(self, request, *args, **kwargs):
        dto = serializer.validate(request.data)
        result = self.container.create_assignment.execute(dto)
        return presenter.to_http_response(result)
```

**Principio aplicado:** DIP + Composition Root + Dependency Rule  
**Beneficio:** El controlador deja de conocer implementaciones concretas. Se puede testear con mocks/fakes sin levantar Django ni RabbitMQ.

---

### 4.2 [ERR-01] Manejo de Excepciones por Frontera — Error Mapping por Capas

**Estado Actual** (monolito):
Fuente: `assignments/infrastructure/repository.py` (líneas 19-31)

```python
def save(self, assignment: Assignment) -> Assignment:
    if assignment.id:
        model = TicketAssignmentModel.objects.get(id=assignment.id)  # ← Sin try/except
        model.priority = assignment.priority
        model.assigned_to = assignment.assigned_to
        model.save()
    else:
        model = TicketAssignmentModel.objects.create(...)
    return self._to_entity(model)
```

**Estado Propuesto** (Clean Architecture):

```python
# === Entities (Domain) ===
# assignments/domain/exceptions.py
class DomainException(Exception): pass
class AssignmentNotFound(DomainException): pass

# === Interface Adapter (Repository) ===
# assignments/infrastructure/repository.py
def save(self, assignment: Assignment) -> Assignment:
    if assignment.id is None:
        model = TicketAssignmentModel.objects.create(...)
        return self._to_entity(model)

    try:
        model = TicketAssignmentModel.objects.get(id=assignment.id)
    except TicketAssignmentModel.DoesNotExist as exc:
        raise AssignmentNotFound(f"Assignment {assignment.id} not found") from exc

    model.priority = assignment.priority
    model.assigned_to = assignment.assigned_to
    model.save()
    return self._to_entity(model)

# === Application (Use Case) ===
try:
    saved = repository.save(assignment)
except AssignmentNotFound:
    return ApplicationResult.not_found("Assignment not found")

# === Interface Adapter (View) ===
# Mapea ApplicationResult.not_found → HTTP 404
```

**Principio aplicado:** SRP + DIP (dominio define semántica, infraestructura traduce)  
**Beneficio:** Evita error 500 inesperado ante IDs huérfanos. El caso de uso responde con error de negocio explícito y consistente.

---

### 4.3 [EDA-01] ACK Post-Procesamiento — Boundary Control

**Estado Actual** (monolito):
Fuente: `messaging/consumer.py` (líneas 54-66)

```python
def callback(ch, method, properties, body):
    try:
        event_data = json.loads(body)
        process_ticket_event.delay(event_data)                       # ← Fire-and-forget
        logger.info("Event received and sent to Celery: %s", event_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)               # ← ACK prematuro
    except Exception as e:
        logger.error("Error processing message: %s", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

**Estado Propuesto** (Clean Architecture):

```python
# === Application Port ===
# application/ports/message_processor.py
class MessageProcessorPort(Protocol):
    def process(self, event_data: dict) -> ProcessingResult: ...

# === Frameworks & Drivers (Consumer) ===
# messaging/consumer.py
def callback(ch, method, properties, body):
    try:
        event_data = json.loads(body)
        result = processor.process(event_data)   # ← Síncrono, espera resultado
        if result.success:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # → DLQ
    except TransientProcessingError:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Reintento
    except Exception:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # → DLQ
```

**Principio aplicado:** Boundary Control en adapters + SRP  
**Beneficio:** El ACK representa "procesado real", no "encolado". Reduce pérdida silenciosa de mensajes y mejora la confiabilidad operacional.

---

### 4.4 [CFG-01] Externalización de Credenciales — Configuración como Detalle

**Estado Actual** (monolito):
Fuente: `assessment_service/settings.py` (líneas 136-137)

```python
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
CELERY_RESULT_BACKEND = 'rpc://'
```

**Estado Propuesto** (Clean Architecture):

```python
# === Frameworks & Drivers (Settings) ===
# assessment_service/settings.py
from django.core.exceptions import ImproperlyConfigured

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ImproperlyConfigured(f"Variable de entorno requerida: {name}")
    return value

RABBITMQ_USER = require_env("RABBITMQ_USER")
RABBITMQ_PASSWORD = require_env("RABBITMQ_PASSWORD")
RABBITMQ_HOST = require_env("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")

CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}"
    f"@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
)
```

**Principio aplicado:** Separation of Concerns (configuración ≠ código) + 12-Factor App  
**Beneficio:** Elimina secretos del código fuente. Permite variar credenciales por entorno (dev/staging/prod) sin tocar código.

---

### 4.5 [SCL-01] Paginación Global — Política de Framework

**Estado Actual** (monolito):
Fuente: `assessment_service/settings.py` (líneas 162-169), `assignments/views.py` (línea 27)

```python
# settings.py — Sin paginación configurada
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (...),
    'DEFAULT_PERMISSION_CLASSES': (...),
}

# views.py — Queryset completo sin límite
queryset = TicketAssignment.objects.all().order_by('-assigned_at')
```

**Estado Propuesto** (Clean Architecture):

```python
# === Frameworks & Drivers (DRF Settings) ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (...),
    'DEFAULT_PERMISSION_CLASSES': (...),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('API_PAGE_SIZE', '20')),
}

# Contrato de respuesta esperado:
# { "count": 150, "next": "?page=2", "previous": null, "results": [...] }
```

**Principio aplicado:** OCP + centralización de políticas en capa de framework  
**Beneficio:** Rendimiento predecible. Protección contra degradación con volúmenes altos. Contrato de API estándar para el consumidor.

---

### 4.6 [SLD-02] Excepciones de Dominio Expresivas — Lenguaje Ubicuo

**Estado Actual** (monolito):
Fuente: `assignments/domain/entities.py` (líneas 33-52)

```python
def _validate(self):
    if not self.ticket_id or not self.ticket_id.strip():
        raise ValueError("ticket_id es requerido y no puede estar vacío")

    if self.priority not in self.VALID_PRIORITIES:
        raise ValueError(
            f"priority debe ser uno de {self.VALID_PRIORITIES}, "
            f"recibido: {self.priority}"
        )
```

**Estado Propuesto** (Clean Architecture):

```python
# === Entities (Domain) — Excepciones semánticas ===
# assignments/domain/exceptions.py
class DomainException(Exception):
    """Base para todas las excepciones de dominio."""
    pass

class ValidationError(DomainException):
    """Error de validación de reglas de negocio."""
    pass

class EmptyTicketId(ValidationError):
    """El ticket_id no puede estar vacío."""
    pass

class InvalidPriority(ValidationError):
    """La prioridad proporcionada no es válida."""
    pass

# === Entities (Domain) — Entidad con validación expresiva ===
# assignments/domain/entities.py
def _validate(self):
    if not self.ticket_id or not self.ticket_id.strip():
        raise EmptyTicketId("ticket_id es requerido y no puede estar vacío")

    if self.priority not in self.VALID_PRIORITIES:
        raise InvalidPriority(
            f"priority debe ser uno de {self.VALID_PRIORITIES}, "
            f"recibido: {self.priority}"
        )

def change_priority(self, new_priority: str) -> None:
    if new_priority not in self.VALID_PRIORITIES:
        raise InvalidPriority(new_priority)

# === Interface Adapter (View) — Mapeo semántico ===
# assignments/views.py
except EmptyTicketId as e:
    return Response({"error": str(e), "code": "empty_ticket_id"}, status=400)
except InvalidPriority as e:
    return Response({"error": str(e), "code": "invalid_priority"}, status=400)
```

**Principio aplicado:** Lenguaje Ubicuo del Dominio + SRP + DIP  
**Beneficio:** Los errores expresan intención de negocio (no técnica genérica). Facilita mapeo consistente a HTTP, observabilidad y pruebas unitarias de reglas de dominio.

---

## 5. Conclusión

### Impacto Esperado en la Agilidad del Equipo

Adoptar Clean Architecture de forma explícita, según Robert C. Martin, ataca la **raíz** de la deuda técnica observada: acoplamiento estructural, errores poco semánticos y fragilidad operativa en mensajería/configuración.

La combinación de **Dependency Rule + SOLID + separación de capas** produce los siguientes beneficios medibles:

| Dimensión | Estado Actual (Monolito) | Estado Objetivo (Clean Architecture) |
|---|---|---|
| **Lead Time** | Cambios funcionales requieren tocar presentación + infraestructura | Cambios localizados en la capa afectada |
| **Tasa de regresiones** | Alta — dependencias cruzadas propagan fallos | Baja — capas aisladas con contratos claros |
| **Testabilidad** | Requiere DB + broker + servidor web para probar lógica | Dominio y casos de uso testeables sin infraestructura |
| **Onboarding** | Complejo — todo está interconectado | Modular — cada capa tiene responsabilidad clara |
| **Seguridad** | Credenciales en código, configuración permisiva | Secretos externalizados, defaults seguros |
| **Resiliencia** | Pérdida de mensajes, sin reintentos | ACK post-procesamiento, retry explícito |
| **Escalabilidad** | Sin paginación, conexión nueva por mensaje | Paginación global, conexiones reutilizables |

### Resumen

Los 18+ dolores identificados no son problemas aislados — son **síntomas de violaciones sistemáticas** a la Dependency Rule y los principios SOLID. La migración a Clean Architecture no es un ejercicio teórico: es la estrategia más directa para reducir el costo de cambio, mejorar la confiabilidad y permitir que el equipo evolucione el sistema sin miedo a romper lo que ya funciona.

> *"La arquitectura de un sistema de software es la forma que le dan aquellos que lo construyen. La forma se define por la división del sistema en componentes, la disposición de esos componentes y la manera en que se comunican entre sí."*  
> — Robert C. Martin, *Clean Architecture* (2017)

## 1) Introducción

El monolito **Assignment Service** (Django + DDD + EDA) ya muestra intenciones de separación por capas, pero todavía conserva acoplamientos fuertes a framework, infraestructura y configuración operativa que frenan su evolución. El objetivo de migración es consolidar una **Clean Architecture** explícita, siguiendo a **Robert C. Martin (Uncle Bob)**: reglas de negocio en el centro, detalles técnicos en la periferia y dependencias siempre apuntando hacia adentro (**Dependency Rule**).

Este documento funciona como plan de implementación colaborativo entre agentes (Planner, Coder y Designer), mapeando cada dolor detectado a principios arquitectónicos y proponiendo una ruta de trabajo incremental para mejorar mantenibilidad, testabilidad, seguridad y resiliencia operativa.

---

## 2) Plan por agentes (pasos numerados con asignación de archivos)

### Paso 1 — Baseline y trazabilidad de dolores
- **Agente:** Planner
- **Objetivo:** Confirmar alcance y severidad de todos los dolores, sin omitir ninguno.
- **Archivos a leer:**
  - `DOLORES.md`
  - `ARCHITECTURE_DDD.md`
  - `README.md`
- **Entregable:** Matriz completa Dolor → Principio CA → Beneficio.

### Paso 2 — Validación externa de lineamientos técnicos
- **Agente:** Planner
- **Objetivo:** Verificar criterios de seguridad/paginación y alinearlos al debate arquitectónico.
- **Fuentes a contrastar:**
  - Robert C. Martin (Clean Architecture)
  - Django docs (`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`)
  - Django REST Framework docs (paginación global)
- **Entregable:** Argumentación técnica no basada en supuestos.

### Paso 3 — Mapeo comparativo completo (todos los dolores)
- **Agente:** Planner
- **Objetivo:** Relacionar cada dolor con principios CA/SOLID aplicables y beneficio concreto.
- **Archivos base para análisis:**
  - `assignments/views.py`
  - `messaging/handlers.py`
  - `assignments/infrastructure/repository.py`
  - `assignments/infrastructure/messaging/event_publisher.py`
  - `assignments/infrastructure/messaging/event_adapter.py`
  - `messaging/consumer.py`
  - `assignments/tasks.py`
  - `assignments/tests.py`
  - `assignments/test_integration.py`
  - `assessment_service/settings.py`
  - `Dockerfile`
  - `assignments/domain/entities.py`
  - `assessment_service/urls.py`
  - `messaging/test_consumer_reconnection.py`
  - `messaging/test_dead_letter_queue.py`
  - `assignments/migrations/0001_initial.py`
  - `assignments/infrastructure/django_models.py`
- **Entregable:** Sección 3 (tabla comparativa completa).

### Paso 4 — Diseño de arquitectura objetivo por capas
- **Agente:** Designer
- **Objetivo:** Definir layout profesional del documento y visualización de capas CA.
- **Archivos de referencia:**
  - `ARCHITECTURE_DDD.md`
  - `INDEX.md`
- **Entregable:** Plantilla editorial + diagrama textual de capas + criterios visuales.

### Paso 5 — Plan de ejecución técnica para 6 dolores críticos
- **Agente:** Coder
- **Objetivo:** Preparar pseudocódigo CA para dolores críticos: `CPL-01`, `ERR-01`, `EDA-01`, `CFG-01`, `SCL-01`, `SLD-02`.
- **Archivos a leer obligatoriamente (contexto):**
  - `assignments/views.py`
  - `assignments/infrastructure/repository.py`
  - `messaging/consumer.py`
  - `assessment_service/settings.py`
  - `assignments/domain/entities.py`
  - `assignments/domain/repository.py`
  - `assignments/application/event_publisher.py`
  - `assignments/application/use_cases/create_assignment.py`
  - `assignments/application/use_cases/reassign_ticket.py`
- **Entregable:** Sección 5 (pseudocódigo estructurado por capas CA).

### Paso 6 — Cierre de debate e impacto esperado
- **Agente:** Planner
- **Objetivo:** Enlazar mejoras arquitectónicas con agilidad de desarrollo y reducción de riesgo.
- **Archivos de soporte:**
  - `DOLORES.md`
  - `USAGE_GUIDE.md`
- **Entregable:** Conclusión ejecutiva con impacto técnico y operativo.

---

## 3) Análisis comparativo completo (Dolor vs Principio CA vs Beneficio)

> Referencia explícita: **Robert C. Martin (Uncle Bob)**. El enfoque aplicado usa **Dependency Rule**, separación de capas y principios **SOLID** (SRP, OCP, LSP, ISP, DIP) para desacoplar reglas de negocio de UI, DB, broker y framework.

| Dolor | Principio(s) Clean Architecture / SOLID | Beneficio concreto esperado |
|---|---|---|
| **CPL-01** ViewSet instancia repositorio/publisher concretos | Dependency Rule, **DIP**, SRP | Cambiar Django/RabbitMQ sin tocar casos de uso; tests de aplicación sin framework |
| **CPL-02** Handler crea dependencias por evento | **DIP**, SRP, OCP | Menor acoplamiento por mensaje; composición centralizada de dependencias |
| **DUP-01** Integración duplicada en dos archivos | SRP, OCP | Menos costo de mantenimiento y menor riesgo de divergencia entre suites |
| **ERR-01** `save()` update sin manejar `DoesNotExist` | SRP, manejo de errores por frontera, DIP | Fallas controladas de dominio/aplicación en vez de 500 opacos |
| **ERR-02** `except Exception` genérico en publisher/adapter | SRP, ISP (errores específicos) | Observabilidad y políticas de recuperación diferenciadas |
| **ERR-03** Reconexión captura todo error | SRP, OCP | Retry solo para fallas transitorias; errores de programación fallan rápido |
| **MOD-01** God test file mezclando capas/estilos | SRP, separación de capas | Suite legible, modular y estable por contexto (dominio/app/infra/API) |
| **CFG-01** Credenciales RabbitMQ hardcodeadas | Frameworks & Drivers como detalle, Dependency Rule, DIP | Seguridad por entorno y despliegue portable |
| **CFG-02** CMD mezcla migración + worker | SRP, separación de responsabilidades operativas | Operación escalable por proceso (web/worker/migrate) |
| **TST-01** Tests replican lógica interna del consumer | Testabilidad de casos de uso/adapters, OCP | Evita falsos positivos; valida comportamiento real del sistema |
| **TST-02** URLs de tests no coinciden con router real | Interface Adapters como contrato, SRP | Coherencia entre API pública y pruebas de aceptación |
| **SCL-01** Sin paginación global | OCP, SRP en capa de presentación | Rendimiento estable con dataset grande y menor presión de red |
| **SCL-02** Nueva conexión RabbitMQ por evento | SRP en infraestructura, OCP | Mayor throughput y menor latencia bajo carga |
| **SLD-01** Se inyecta `event_publisher` pero no se usa | **ISP**, DIP, SRP | Contratos más precisos y menor deuda cognitiva |
| **SLD-02** Dominio usa `ValueError` genérico | SRP, lenguaje ubicuo del dominio, DIP | Errores semánticos de negocio y mejor traducción a API |
| **NOM-01** Docstring con término incorrecto | SRP (claridad), cohesión semántica | Menor ambigüedad para desarrollo y soporte |
| **NOM-02** Import muerto (`random`) | SRP, limpieza de dependencias | Menos ruido y menor riesgo de mantenimiento accidental |
| **DOC-01** Serializer sin validadores explícitos | Interface Adapters (validación en borde), SRP | Contrato HTTP claro antes de entrar al dominio |
| **SEC-01** `ALLOWED_HOSTS` vacío con `DEBUG=False` | Fail-safe defaults, políticas explícitas separadas del framework | Menor exposición a ataques por Host header |
| **SEC-02** Fallback CSRF permisivo no condicionado por entorno | Políticas explícitas por entorno, SRP de configuración | Menor riesgo de configuración insegura en no-dev |
| **EDA-01** ACK prematuro antes de confirmar procesamiento | Boundary control en adapters, SRP, DIP | Reduce pérdida de mensajes; trazabilidad real del procesamiento |
| **EDA-02** Celery sin retry/backoff explícito | OCP, SRP (resiliencia en infraestructura) | Tolerancia a fallos transitorios y mayor confiabilidad |
| **EDA-03** Inconsistencia de routing key DLQ | Contratos explícitos entre adapters, OCP | Menos incidentes operativos por mismatch de enrutamiento |
| **DEB-01** Divergencia migración vs modelo (`assigned_at`) | Single source of truth de persistencia, SRP | Menos drift entre entornos y despliegues predecibles |

### Debate clave: independencia de Framework/UI/DB

- Si **Django/DRF/RabbitMQ/PostgreSQL** son detalles externos, el núcleo (entidades + casos de uso) no se rompe al cambiar tecnología.
- Al mover políticas al centro, las decisiones de framework se vuelven reversibles y de menor costo.
- La testabilidad mejora porque los casos de uso se ejecutan sin servidor web, sin broker y sin ORM real.
- El mantenimiento deja de ser “cambio transversal” y pasa a ser “cambio localizado por capa”.

---

## 4) Propuesta de capas Clean Architecture (distribución objetivo)

## 4.1 Mapa de capas

```text
┌─────────────────────────────────────────────────────────────┐
│ Frameworks & Drivers                                       │
│ Django, DRF, ORM Model, RabbitMQ, Celery, Settings, Docker │
└───────────────▲─────────────────────────────────────────────┘
                │ implementa puertos
┌───────────────┴─────────────────────────────────────────────┐
│ Interface Adapters                                          │
│ Views, Serializers, Repositorios concretos, Event Adapters  │
└───────────────▲─────────────────────────────────────────────┘
                │ llama casos de uso / traduce DTOs
┌───────────────┴─────────────────────────────────────────────┐
│ Application (Use Cases)                                     │
│ CreateAssignment, ReassignTicket, ChangePriority, etc.      │
│ + Puertos: AssignmentRepository, EventPublisher             │
└───────────────▲─────────────────────────────────────────────┘
                │ reglas de negocio puras
┌───────────────┴─────────────────────────────────────────────┐
│ Entities (Domain)                                           │
│ Assignment, DomainEvents, DomainExceptions                  │
└─────────────────────────────────────────────────────────────┘
```

## 4.2 Asignación de código actual a capas

- **Entities:** `assignments/domain/entities.py`, `assignments/domain/events.py`
- **Use Cases:** `assignments/application/use_cases/*.py`
- **Ports (abstracciones):**
  - `assignments/domain/repository.py`
  - `assignments/application/event_publisher.py`
- **Interface Adapters:**
  - `assignments/views.py`
  - `assignments/serializers.py`
  - `assignments/infrastructure/repository.py` (adapter a ORM)
  - `assignments/infrastructure/messaging/event_adapter.py`
- **Frameworks & Drivers:**
  - `assessment_service/settings.py`
  - `assignments/infrastructure/django_models.py`
  - `messaging/consumer.py`
  - `assignments/tasks.py`
  - `Dockerfile`

## 4.3 Criterios de diseño (Designer)

1. Encabezados con numeración jerárquica estable (1, 1.1, 1.2…).
2. Tablas con 3 columnas fijas para comparación (Dolor, Principio, Beneficio).
3. Bloques de pseudocódigo con estructura por capas (Entities, Use Case, Adapter, Driver).
4. Etiquetas de criticidad visibles (`Alta`, `Media`, `Baja`) para priorización.
5. Sección final con impacto en negocio (lead time, incidentes, calidad de releases).

---

## 5) Pseudocódigo de solución (6 dolores críticos)

> Objetivo: mostrar **qué** estructura debe implementar Coder en términos CA, no código final de producción.

### 5.1 `CPL-01` — ViewSet acoplado a concretos (DIP)

**Archivos de contexto a leer (Coder):**
- `assignments/views.py`
- `assignments/domain/repository.py`
- `assignments/application/event_publisher.py`
- `assignments/application/use_cases/create_assignment.py`

```text
[Composition Root / Framework]
build_container():
  repo = DjangoAssignmentRepository()
  publisher = RabbitMQEventPublisher()
  create_assignment_uc = CreateAssignment(repo, publisher)
  return container

[Interface Adapter: View]
create(request):
  dto = serializer.validate(request.data)
  result = container.create_assignment_uc.execute(dto)
  return presenter.to_http_response(result)

[Application]
CreateAssignment.execute(cmd):
  assignment = Assignment.create(cmd.ticket_id, cmd.priority, cmd.assigned_to)
  saved = repository.save(assignment)
  event_publisher.publish(saved.pull_events())
  return saved
```

---

### 5.2 `ERR-01` — update sin manejo de `DoesNotExist`

**Archivos de contexto a leer (Coder):**
- `assignments/infrastructure/repository.py`
- `assignments/domain/entities.py`
- `assignments/application/use_cases/reassign_ticket.py`

```text
[Domain]
class AssignmentNotFound(DomainException)

[Infrastructure Repository Adapter]
save(assignment):
  if assignment.id exists:
    try find ORM model by id
    if not found: raise AssignmentNotFound(assignment.id)
    update fields and persist
  else:
    create model
  return to_domain(model)

[Application]
use_case.execute(cmd):
  try:
    return repository.save(entity)
  except AssignmentNotFound as e:
    raise ApplicationError.not_found(e)

[Interface Adapter: View]
map ApplicationError.not_found -> HTTP 404
```

---

### 5.3 `EDA-01` — ACK prematuro en consumer

**Archivos de contexto a leer (Coder):**
- `messaging/consumer.py`
- `assignments/tasks.py`
- `messaging/handlers.py`

```text
[Framework Driver: Rabbit Consumer]
callback(message):
  event = deserialize(message.body)
  task = process_ticket_event.apply_async(event, correlation_id)

  if task completed successfully:
    basic_ack(delivery_tag)
  else:
    basic_nack(delivery_tag, requeue=False)  # DLQ

[Application/Infra policy]
process_ticket_event:
  execute idempotent handler
  return Success/Failure explicit status

[Operational]
trace message_id + correlation_id for retry safety
```

---

### 5.4 `CFG-01` — credenciales RabbitMQ hardcodeadas

**Archivos de contexto a leer (Coder):**
- `assessment_service/settings.py`
- `Dockerfile`
- `assessment_service/celery.py`

```text
[Frameworks & Drivers: Settings]
RABBIT_USER = env("RABBITMQ_USER", required=True)
RABBIT_PASS = env("RABBITMQ_PASSWORD", required=True)
RABBIT_HOST = env("RABBITMQ_HOST", required=True)
CELERY_BROKER_URL = build_amqp_url(RABBIT_USER, RABBIT_PASS, RABBIT_HOST)

if DEBUG is False and any required value missing:
  raise ImproperlyConfigured

[Deployment]
inject credentials by environment (.env / secrets manager)
never fallback to guest:guest in non-dev
```

---

### 5.5 `SCL-01` — sin paginación global

**Archivos de contexto a leer (Coder):**
- `assessment_service/settings.py`
- `assignments/views.py`
- `assignments/serializers.py`

```text
[Frameworks & Drivers: DRF Settings]
REST_FRAMEWORK.DEFAULT_PAGINATION_CLASS = "rest_framework.pagination.PageNumberPagination"
REST_FRAMEWORK.PAGE_SIZE = 20

[Interface Adapter: ViewSet]
list():
  queryset ordered and filtered
  paginator applies globally
  return paginated response

[Expected Contract]
response = {count, next, previous, results[]}
```

---

### 5.6 `SLD-02` — ValueError genérico en dominio

**Archivos de contexto a leer (Coder):**
- `assignments/domain/entities.py`
- `assignments/views.py`
- `assignments/application/use_cases/change_assignment_priority.py`

```text
[Domain]
class DomainException
class InvalidPriority(DomainException)
class InvalidTicketId(DomainException)

Assignment.validate():
  if ticket_id invalid -> raise InvalidTicketId
  if priority invalid -> raise InvalidPriority

[Application]
catch DomainException and map to application result (validation error)

[Interface Adapter: View]
map InvalidPriority/InvalidTicketId -> HTTP 400 with stable error schema
```

---

## 6) Conclusión

Adoptar Clean Architecture de forma explícita, según Robert C. Martin, ataca la raíz de la deuda técnica observada: acoplamiento estructural, errores poco semánticos y fragilidad operativa en mensajería/configuración. La combinación de **Dependency Rule + SOLID + separación de capas** reduce el costo de cambio, mejora la confiabilidad de pruebas y permite evolucionar framework, broker o DB sin rehacer el núcleo de negocio.

En términos de agilidad, el impacto esperado es: menor lead time para cambios funcionales, menor tasa de regresiones por dependencias cruzadas y mejor capacidad de operar en producción con políticas de seguridad y resiliencia explícitas.
