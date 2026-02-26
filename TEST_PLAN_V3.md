$$# TEST PLAN V3 — Assignment Service

> **Proyecto:** backend-assignment-service  
> **Versión del Plan:** 3.0  
> **Fecha:** 2026-02-26  
> **Stack Tecnológico:** Django 6.0.2 · DRF · Celery · RabbitMQ · PostgreSQL  
> **Arquitectura:** Domain-Driven Design (DDD) + Event-Driven Architecture (EDA)  
> **Referencia de Requisitos:** [USERSTORIES Y CRITERIOS DE ACEPTACION.md](USERSTORIES%20Y%20CRITERIOS%20DE%20ACEPTACION.md)

---

## Tabla de Contenidos

1. [Objetivo del Plan](#1-objetivo-del-plan)
2. [Alcance de Pruebas](#2-alcance-de-pruebas)
3. [Niveles de Prueba](#3-niveles-de-prueba)
4. [Mapeo ISO/IEC 25010:2023](#4-mapeo-isoiec-250102023)
5. [Herramientas y Stack de Testing](#5-herramientas-y-stack-de-testing)
6. [Estrategia de Cobertura](#6-estrategia-de-cobertura)
7. [Calendario de Pruebas](#7-calendario-de-pruebas)
8. [Gestión de Riesgos](#8-gestión-de-riesgos)
9. [Trazabilidad INVEST → Pruebas](#9-trazabilidad-invest--pruebas)
10. [Criterios de Entrada y Salida](#10-criterios-de-entrada-y-salida)
11. [Roles y Responsabilidades](#11-roles-y-responsabilidades)
12. [Apéndice A — Comandos de Ejecución](#apéndice-a--comandos-de-ejecución)

---

## 1. Objetivo del Plan

Definir la estrategia, alcance, herramientas, calendario y gestión de riesgos para asegurar la calidad del **assignment-service** conforme a:

- Los **10 User Stories** definidos en [USERSTORIES Y CRITERIOS DE ACEPTACION.md](USERSTORIES%20Y%20CRITERIOS%20DE%20ACEPTACION.md), validados con principios **INVEST**.
- El estándar de calidad de software **ISO/IEC 25010:2023**, mapeando cada característica de calidad a actividades de prueba concretas.
- La arquitectura **DDD + EDA** del servicio, probando cada capa de forma independiente y su integración.

---

## 2. Alcance de Pruebas

### 2.1 Dentro del Alcance (In-Scope)

| Capa DDD | Componentes | Qué se prueba |
|----------|-------------|---------------|
| **Dominio** | `Assignment` entity, `DomainEvent`s, validaciones | Reglas de negocio puras, máquina de estados de prioridad, generación de eventos |
| **Aplicación** | `CreateAssignment`, `ReassignTicket`, `ChangeAssignmentPriority`, `UpdateAssignedUser` | Orquestación de casos de uso, inyección de dependencias, flujo comando→resultado |
| **Infraestructura** | `DjangoAssignmentRepository`, `RabbitMQEventPublisher`, `TicketEventAdapter`, consumer, DLQ | Persistencia ORM, publicación/consumo de eventos, Dead Letter Queue, reconexión |
| **Presentación** | `TicketAssignmentViewSet`, `TicketAssignmentSerializer` | Endpoints REST, serialización, validación HTTP, códigos de respuesta |
| **Tareas Asíncronas** | `process_ticket_event` (Celery task) | Delegación a handlers, ejecución eager en tests |
| **CI/CD** | `.github/workflows/ci.yml` | Pipeline GH Actions, ejecución de tests, reporte de cobertura, linting |

### 2.2 Fuera del Alcance (Out-of-Scope)

| Elemento | Razón |
|----------|-------|
| Código del `ticket-service` | Microservicio independiente; se simula con mocks y mensajes de prueba |
| Interfaz de usuario / frontend | No existe en este servicio; es API pura |
| Pruebas de carga / stress | Fuera del alcance del taller; se documenta como riesgo de producto |
| Seguridad avanzada (pen-testing) | Se cubren validaciones de entrada y XSS; pen-testing queda diferido |

---

## 3. Niveles de Prueba

### 3.1 Pruebas Unitarias (Unit Tests)

**Objetivo:** Validar reglas de negocio de la capa de dominio en aislamiento completo.

| Aspecto | Detalle |
|---------|---------|
| **Capa objetivo** | Dominio (`entities.py`, `events.py`) |
| **Dependencias externas** | Ninguna — sin Django, sin BD, sin broker |
| **Framework** | pytest + pytest-django |
| **Ubicación** | `assignments/tests/test_assignments.py` → clases `AssignmentEntityTests`, `DomainEventsTests` |
| **Velocidad** | < 1 segundo para toda la suite de dominio |

**Componentes cubiertos:**

| Componente | Tests Clave |
|------------|-------------|
| `Assignment` entity | Creación válida, validación `ticket_id` vacío/espacios, prioridad inválida, `change_priority()` válida/inválida |
| `Assignment.VALID_PRIORITIES` | Aceptación de `high`, `medium`, `low`, `unassigned` |
| `AssignmentCreated` event | Serialización `to_dict()`, campos correctos, `event_type` |
| `AssignmentReassigned` event | Serialización con `old_priority` y `new_priority` |

### 3.2 Pruebas de Integración (Integration Tests)

**Objetivo:** Validar la interacción entre capas — repositorio ↔ BD, casos de uso ↔ repositorio, API ↔ caso de uso.

| Aspecto | Detalle |
|---------|---------|
| **Capas objetivo** | Aplicación + Infraestructura + Presentación |
| **Dependencias** | PostgreSQL (test DB via Django TestCase), mocks para RabbitMQ |
| **Framework** | pytest-django con `@override_settings`, `APIClient` de DRF |
| **Ubicación** | `assignments/tests/test_assignments.py` → clases de API y repositorio |

**Componentes cubiertos:**

| Componente | Tests Clave |
|------------|-------------|
| `DjangoAssignmentRepository` | `save()` persiste en BD, `find_by_id()` retorna dominio, `find_all()` con orden, `delete()` |
| `CreateAssignment` use case | Creación completa ticket→BD→evento, idempotencia por `ticket_id` |
| `ReassignTicket` use case | Cambio de prioridad con evento, misma prioridad sin evento, ticket inexistente |
| `UpdateAssignedUser` use case | Asignar, reasignar, desasignar usuario |
| `TicketEventAdapter` | Traducción evento externo → caso de uso, eventos `ticket.created` y `ticket.priority_changed` |
| `TicketAssignmentViewSet` | POST `/assignments/`, GET `/assignments/`, GET `/assignments/{id}/`, POST `/assignments/reassign/`, PATCH `/assignments/{id}/assign-user/`, DELETE `/assignments/{id}/` |
| `process_ticket_event` task | Ejecución Celery eager, delegación a handlers |
| `TicketAssignmentSerializer` | Validación de campos, prioridades válidas, serialización |

### 3.3 Pruebas End-to-End (E2E)

**Objetivo:** Validar el flujo completo: mensaje RabbitMQ → consumer → Celery → handler → BD → evento publicado.

| Aspecto | Detalle |
|---------|---------|
| **Capas objetivo** | Todas — broker real, BD real, procesamiento completo |
| **Dependencias** | RabbitMQ real, PostgreSQL real (docker-compose) |
| **Herramienta** | `assignments/test_integration.py` + **Postman** (colección manual) |
| **Entorno** | `docker-compose up` con todos los servicios |

**Flujos E2E cubiertos:**

| Flujo | Descripción |
|-------|-------------|
| RabbitMQ → DB | Publicar mensaje en cola → consumer ACK → Celery task → asignación creada en BD |
| API → DB → Evento | POST API → caso de uso → BD → evento publicado en exchange |
| DLQ | Mensaje malformado → NACK → enrutado a Dead Letter Queue |
| Reconexión broker | Pérdida de conexión → backoff exponencial → reconexión automática |

### 3.4 Pirámide de Testing

```
         ╱ ╲
        ╱ E2E ╲         ← Pocos tests, máximo costo, flujo completo
       ╱───────╲            (Postman + test_integration.py)
      ╱ Integr.  ╲      ← Tests moderados, BD + mocks broker
     ╱─────────────╲        (pytest-django + APIClient)
    ╱   Unitarios    ╲   ← Máximos tests, cero dependencias, rápidos
   ╱───────────────────╲    (pytest puro sobre dominio)
```

---

## 4. Mapeo ISO/IEC 25010:2023

El estándar ISO/IEC 25010:2023 define **8 características de calidad** del producto software. A continuación se mapea cada una a actividades de prueba concretas del assignment-service.

### 4.1 Tabla de Cobertura ISO/IEC 25010:2023

| # | Característica | Sub-característica | Actividad de Prueba | Nivel | US Relacionada |
|---|---------------|-------------------|---------------------|-------|----------------|
| 1 | **Adecuación Funcional** | Completitud funcional | Verificar que los 10 US tienen tests que cubren todos los escenarios Gherkin | Unit + Integration | US-01 a US-10 |
| 1 | | Corrección funcional | Validar resultados exactos: códigos HTTP, campos de respuesta, estados en BD | Integration | US-01 a US-06 |
| 1 | | Pertinencia funcional | Confirmar que solo se exponen los endpoints definidos en el contrato API | Integration | US-01 a US-06 |
| 2 | **Eficiencia de Desempeño** | Comportamiento temporal | Medir tiempo de respuesta de endpoints bajo carga normal (< 200ms p95) | E2E (Postman) | US-01, US-02 |
| 2 | | Utilización de recursos | Monitorear uso de memoria del worker Celery y consumer RabbitMQ | Observabilidad | US-07, US-08 |
| 2 | | Capacidad | Verificar procesamiento de ráfagas de eventos sin pérdida de mensajes | E2E | US-07 |
| 3 | **Compatibilidad** | Coexistencia | Verificar que el servicio opera junto a ticket-service sin interferencia de BD/colas | E2E (docker-compose) | US-09 |
| 3 | | Interoperabilidad | Validar formato de eventos publicados/consumidos según contrato inter-servicio | Integration | US-07, US-08 |
| 4 | **Usabilidad** | Reconocibilidad de adecuación | Verificar que los endpoints retornan mensajes de error descriptivos | Integration | US-01, US-04 |
| 4 | | Protección contra errores de usuario | Validar rechazo de entradas inválidas (prioridad incorrecta, ticket_id vacío, JSON malformado) | Unit + Integration | US-01, US-04, US-07 |
| 5 | **Fiabilidad** | Madurez | Ejecutar suite completa sin fallos intermitentes (flaky tests = 0) | CI (GH Actions) | US-10 |
| 5 | | Disponibilidad | Verificar reconexión automática del consumer RabbitMQ tras caída del broker | Integration | US-07 |
| 5 | | Tolerancia a fallos | Validar DLQ para mensajes malformados; idempotencia en creación de asignaciones | Integration + E2E | US-07 |
| 5 | | Recuperabilidad | Confirmar persistencia de datos tras reinicio de contenedores (volúmenes PostgreSQL) | E2E | US-09 |
| 6 | **Seguridad** | Confidencialidad | Verificar que endpoints requieren autenticación JWT (excepto en tests con `@override_settings`) | Integration | US-01 a US-06 |
| 6 | | Integridad | Validar que no se pueden inyectar datos malformados que corrompan el estado del dominio | Unit + Integration | US-01, US-04 |
| 6 | | No repudio | Eventos de dominio incluyen timestamps e IDs trazables | Unit | US-07, US-08 |
| 7 | **Mantenibilidad** | Modularidad | Verificar que tests de dominio no importan Django ni infraestructura | Unit | — |
| 7 | | Reusabilidad | Casos de uso inyectan repositorio y publisher; tests usan mocks sin acoplamiento | Unit + Integration | — |
| 7 | | Analizabilidad | Cobertura de código ≥ 70% con reporte detallado (líneas no cubiertas) | CI | US-10 |
| 7 | | Modificabilidad | Agregar un nuevo caso de uso no requiere modificar tests existentes | Diseño | — |
| 7 | | Testabilidad | Cada capa se prueba independientemente gracias a inyección de dependencias | Arquitectura | — |
| 8 | **Portabilidad** | Adaptabilidad | Verificar que `docker-compose up` levanta el ecosistema completo en Linux/macOS/Windows | E2E | US-09 |
| 8 | | Instalabilidad | Confirmar que `docker build` genera imagen funcional sin errores | E2E | US-09 |
| 8 | | Reemplazabilidad | Repositorio abstracto (`AssignmentRepository`) permite cambiar ORM sin afectar dominio | Diseño | — |

### 4.2 Priorización de Características de Calidad

```
┌──────────────────────────┬────────────┬───────────────────────────────────────┐
│ Característica           │ Prioridad  │ Justificación                         │
├──────────────────────────┼────────────┼───────────────────────────────────────┤
│ Adecuación Funcional     │ 🔴 Crítica │ Cumplimiento de requisitos del taller │
│ Fiabilidad               │ 🔴 Crítica │ Tolerancia a fallos en mensajería     │
│ Seguridad                │ 🟡 Alta    │ JWT + validación de entrada           │
│ Mantenibilidad           │ 🟡 Alta    │ Arquitectura DDD evaluada             │
│ Portabilidad             │ 🟡 Alta    │ Contenerización es entregable         │
│ Compatibilidad           │ 🟢 Media   │ Interop con ticket-service            │
│ Usabilidad               │ 🟢 Media   │ Mensajes de error descriptivos        │
│ Eficiencia de Desempeño  │ 🔵 Baja    │ Fuera del alcance principal           │
└──────────────────────────┴────────────┴───────────────────────────────────────┘
```

---

## 5. Herramientas y Stack de Testing

### 5.1 Herramientas Principales

| Herramienta | Versión | Propósito | Configuración |
|-------------|---------|-----------|---------------|
| **pytest** | ≥ 8.0.0 | Runner principal de tests | `pytest.ini` — `DJANGO_SETTINGS_MODULE`, verbosity, `--tb=short` |
| **pytest-django** | ≥ 4.8.0 | Integración Django: TestCase, fixtures, BD de test | Auto-discovery via `conftest.py` + env vars para CI |
| **pytest-cov** | ≥ 5.0.0 | Cobertura de código con umbral mínimo | `--cov=assignments --cov=messaging --cov-fail-under=70` |
| **Postman** | Latest | Pruebas manuales E2E de API REST y colecciones compartidas | Colección exportada en `/docs/postman/` (si aplica) |
| **GitHub Actions** | N/A | CI automatizado — tests + lint + cobertura | `.github/workflows/ci.yml` — PostgreSQL service container |
| **flake8** | Latest | Linting de código Python | Job `lint` en CI — `assignments/`, `messaging/`, `assessment_service/` |
| **unittest.mock** | stdlib | Mocks y patches para aislamiento de dependencias | `@patch('messaging.handlers.RabbitMQEventPublisher')` |
| **DRF APIClient** | 3.16.1 | Cliente HTTP para tests de endpoints REST | `rest_framework.test.APIClient` con `@override_settings` |
| **pika** | ≥ 1.3.0 | Conexión directa a RabbitMQ para tests E2E | Solo en `test_integration.py` (requiere broker real) |

### 5.2 Configuración del Entorno de Test

```
┌─────────────────────────────────────────────────────────────┐
│                    Entorno de Testing                        │
├─────────────────┬───────────────────────────────────────────┤
│ pytest.ini      │ DJANGO_SETTINGS_MODULE, addopts, pattern  │
│ conftest.py     │ Env vars CI-friendly (SECRET_KEY, DB)     │
│ CI (GH Actions) │ PostgreSQL service, Python 3.12, pip      │
│ Local (Docker)  │ docker-compose.yml con backend + PG + RMQ │
└─────────────────┴───────────────────────────────────────────┘
```

### 5.3 Patrón de Mocking Crítico

> **Regla:** Todo test que invoque `handle_ticket_event()` **debe** parchear  
> `'messaging.handlers.RabbitMQEventPublisher'` para evitar conexiones reales a RabbitMQ.

```python
# ✅ Correcto — parchear donde el nombre se busca
@patch('messaging.handlers.RabbitMQEventPublisher')
def test_example(self, mock_publisher):
    handle_ticket_event(event_data)

# ❌ Incorrecto — parchear el módulo original
@patch('assignments.infrastructure.messaging.event_publisher.RabbitMQEventPublisher')
```

---

## 6. Estrategia de Cobertura

### 6.1 Objetivos de Cobertura

| Métrica | Umbral | Aplicación |
|---------|--------|------------|
| **Cobertura global** | ≥ 70% | Fallo del pipeline CI si no se cumple (`--cov-fail-under=70`) |
| **Cobertura dominio** | ≥ 90% | Capa crítica: entidades y eventos |
| **Cobertura aplicación** | ≥ 80% | Casos de uso deben cubrir caminos feliz + error |
| **Cobertura infraestructura** | ≥ 60% | Repositorio y adapters; excluye conexiones reales al broker |
| **Cobertura presentación** | ≥ 70% | Endpoints con todos los códigos de respuesta |

### 6.2 Exclusiones de Cobertura

| Archivo / Patrón | Razón |
|-------------------|-------|
| `assignments/test_integration.py` | Requiere RabbitMQ real; excluido en CI |
| `assignments/tests.py` (legacy) | Suite monolítica legacy; se ejecuta en local |
| `messaging/consumer.py` (líneas de conexión) | Código de infraestructura I/O puro |
| `manage.py`, `wsgi.py`, `asgi.py` | Boilerplate Django |

---

## 7. Calendario de Pruebas

### 7.1 Sprint de Pruebas (Semana 3 del Taller)

```
                     SEMANA 3 — CALENDARIO DE PRUEBAS
 ─────────────────────────────────────────────────────────────
 Día 1 (Lun)  │ Día 2 (Mar)  │ Día 3 (Mié)  │ Día 4 (Jue)  │ Día 5 (Vie)
 ─────────────┼──────────────┼──────────────┼──────────────┼─────────────
 Revisión     │ Ejecución    │ Ejecución    │ Ejecución    │ Reporte
 del plan     │ Unit Tests   │ Integration  │ E2E + Manual │ final
 ─────────────┼──────────────┼──────────────┼──────────────┼─────────────
 • Validar    │ • Dominio    │ • Repos      │ • Docker     │ • Análisis
   alcance    │ • Eventos    │ • Casos uso  │   compose    │   cobertura
 • Preparar   │ • Factory    │ • API REST   │ • Postman    │ • Riesgos
   entorno    │   patterns   │ • Celery     │   colección  │   residuales
 • Revisar    │ • Cobertura  │ • Adapters   │ • DLQ manual │ • Sign-off
   US/Gherkin │   dominio    │   eventos    │ • Reconexión │   del equipo
```

### 7.2 Fases Detalladas

| Fase | Duración | Actividades | Entregable |
|------|----------|-------------|------------|
| **F1 — Planificación** | Día 1 | Revisar TEST_PLAN, validar US, preparar entorno Docker, verificar CI funcional | Entorno listo, plan aprobado |
| **F2 — Pruebas Unitarias** | Día 2 | Ejecutar tests de dominio, validar cobertura ≥90% dominio, corregir defectos | Reporte cobertura dominio |
| **F3 — Pruebas de Integración** | Día 3 | Ejecutar tests de API + repositorio + adapters, validar cobertura global ≥70% | Reporte cobertura global |
| **F4 — Pruebas E2E y Manuales** | Día 4 | Docker-compose up, Postman colección, flujos RabbitMQ→DB, DLQ, reconexión | Evidencia Postman + logs |
| **F5 — Cierre y Reporte** | Día 5 | Consolidar resultados, documentar riesgos residuales, generar reporte final | Reporte final de calidad |

### 7.3 Ejecución Continua (CI)

| Trigger | Qué se ejecuta | Umbral de Fallo |
|---------|----------------|-----------------|
| Push a `main`, `develop`, `feature/**` | Tests unitarios + integración + cobertura + lint | Cobertura < 70% o test fail |
| Pull Request | Mismo pipeline; bloquea merge si falla | Check requerido para merge |

---

## 8. Gestión de Riesgos

### 8.1 Riesgos de Proyecto

Riesgos que afectan la **ejecución del plan de pruebas** (plazo, equipo, infraestructura).

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Contingencia |
|----|--------|:------------:|:-------:|------------|--------------|
| RP-01 | **Plazo insuficiente** para completar las 5 fases de pruebas en la semana del taller | 🟡 Media | 🔴 Alto | Priorizar tests unitarios + integración (F2-F3) que cubren el 80% del valor; E2E es complementario | Entregar con F2+F3 completas y F4 parcial; documentar lo pendiente |
| RP-02 | **Miembro del equipo no disponible** durante la semana de pruebas | 🟡 Media | 🟡 Medio | Documentación de ejecución en este plan; cualquier miembro puede ejecutar los comandos | Redistribuir fases entre miembros disponibles |
| RP-03 | **CI pipeline roto** (GH Actions falla por razones ajenas al código) | 🟢 Baja | 🟡 Medio | Usar `conftest.py` con defaults CI-friendly; PostgreSQL como service container | Ejecutar tests localmente con `docker-compose exec backend pytest` |
| RP-04 | **Entorno Docker no levanta** (conflictos de puertos, imágenes corruptas) | 🟢 Baja | 🔴 Alto | `docker-compose.yml` validado; `.env.example` documentado; volúmenes con nombres explícitos | Ejecutar tests unitarios sin Docker (solo requieren `pytest`); diferir E2E |
| RP-05 | **Dependencia de RabbitMQ real** para tests E2E impide ejecución en CI | 🟡 Media | 🟡 Medio | CI excluye `test_integration.py`; tests de integración usan mocks | Documentar E2E como ejecución manual en entorno Docker |
| RP-06 | **Cambios de última hora en requisitos** que invaliden tests existentes | 🟢 Baja | 🟡 Medio | Tests alineados 1:1 con US validadas (INVEST ✅ 6/6); cambios requieren validación humana | Actualizar tests afectados antes del cierre (F5) |

### 8.2 Riesgos de Producto

Riesgos que afectan la **calidad del software entregado** (bugs, seguridad, rendimiento, datos).

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Característica ISO 25010 |
|----|--------|:------------:|:-------:|------------|--------------------------|
| RD-01 | **Bug en máquina de estados de prioridad** — aceptar prioridades inválidas o transiciones no permitidas | 🟢 Baja | 🔴 Alto | Tests unitarios exhaustivos de `Assignment.change_priority()` con todas las prioridades válidas e inválidas | Adecuación Funcional — Corrección |
| RD-02 | **Pérdida de mensajes** en colas RabbitMQ ante fallos del consumer | 🟡 Media | 🔴 Alto | DLQ implementada con DLX; `basic_nack(requeue=False)` enruta a cola de dead-letter; test de DLQ | Fiabilidad — Tolerancia a fallos |
| RD-03 | **Asignaciones duplicadas** por eventos `ticket.created` repetidos | 🟡 Media | 🟡 Medio | Idempotencia en `CreateAssignment`: verifica existencia por `ticket_id` antes de crear | Fiabilidad — Madurez |
| RD-04 | **Inyección de datos maliciosos** vía campos `ticket_id` o `priority` | 🟢 Baja | 🔴 Alto | Validación en `TicketAssignmentSerializer` + validación de dominio en `Assignment.__post_init__()` | Seguridad — Integridad |
| RD-05 | **Degradación de rendimiento** bajo ráfagas de eventos (colas saturadas) | 🟡 Media | 🟡 Medio | Celery procesa en segundo plano; consumer con prefetch count; monitoreo de cola | Eficiencia de Desempeño — Capacidad |
| RD-06 | **Inconsistencia de datos** entre ticket-service y assignment-service | 🟡 Media | 🔴 Alto | Eventos con timestamps trazables; idempotencia; tolerancia a eventos de tickets desconocidos | Compatibilidad — Interoperabilidad |
| RD-07 | **Pérdida de datos** tras reinicio de contenedores PostgreSQL | 🟢 Baja | 🔴 Alto | Volúmenes Docker persistentes; test de persistencia post-restart en E2E | Fiabilidad — Recuperabilidad |
| RD-08 | **Fallo de reconexión al broker** deja consumer inoperante permanentemente | 🟢 Baja | 🔴 Alto | Backoff exponencial configurable; `MAX_RETRIES=0` (infinito por defecto); test de reconexión | Fiabilidad — Disponibilidad |
| RD-09 | **Regresión funcional** introducida por cambios no cubiertos por tests | 🟡 Media | 🟡 Medio | Cobertura ≥ 70% enforced por CI; pipeline bloquea merge si tests fallan | Mantenibilidad — Analizabilidad |
| RD-10 | **Errores silenciosos** en handlers — excepciones capturadas sin logging ni re-raise | 🟡 Media | 🟡 Medio | Tests verifican que excepciones de dominio se propagan; handlers usan `raise` tras log | Usabilidad — Reconocibilidad |

### 8.3 Matriz de Riesgos (Impacto × Probabilidad)

```
              │  Bajo Impacto  │  Medio Impacto  │  Alto Impacto
──────────────┼────────────────┼─────────────────┼────────────────
Alta Prob.    │                │                 │
──────────────┼────────────────┼─────────────────┼────────────────
Media Prob.   │                │ RP-01, RP-02    │ RD-02, RD-06
              │                │ RP-05, RD-03    │
              │                │ RD-05, RD-09    │
              │                │ RD-10           │
──────────────┼────────────────┼─────────────────┼────────────────
Baja Prob.    │                │ RP-03, RP-06    │ RD-01, RD-04
              │                │                 │ RD-07, RD-08
              │                │                 │ RP-04
```

---

## 9. Trazabilidad INVEST → Pruebas

Cada User Story validada con principios **INVEST** (ver [USERSTORIES Y CRITERIOS DE ACEPTACION.md](USERSTORIES%20Y%20CRITERIOS%20DE%20ACEPTACION.md)) se mapea a pruebas concretas.

### 9.1 Matriz de Trazabilidad US → Tests

| US | Historia | INVEST | Nivel de Prueba | Archivo de Test | Escenarios Gherkin | Riesgo Asociado |
|----|----------|:------:|----------------|-----------------|:------------------:|:---------------:|
| US-01 | Crear asignación vía API | ✅ 6/6 | Unit + Integration | `test_assignments.py` | 4 | RD-01, RD-04 |
| US-02 | Consultar todas las asignaciones | ✅ 6/6 | Integration | `test_assignments.py` | 3 | — |
| US-03 | Consultar asignación por ID | ✅ 6/6 | Integration | `test_assignments.py` | 3 | — |
| US-04 | Reasignar prioridad | ✅ 6/6 | Unit + Integration | `test_assignments.py` | 4 | RD-01, RD-03 |
| US-05 | Asignar/reasignar usuario | ✅ 6/6 | Integration | `test_assignments.py` | 4 | — |
| US-06 | Eliminar asignación | ✅ 6/6 | Integration | `test_assignments.py` | 3 | — |
| US-07 | Creación automática por evento | ✅ 6/6 | Integration + E2E | `test_assignments.py`, `test_integration.py` | 3 | RD-02, RD-03, RD-06 |
| US-08 | Actualización prioridad por evento | ✅ 6/6 | Integration | `test_assignments.py` | 3 | RD-06, RD-10 |
| US-09 | Contenerización Docker | ✅ 6/6 | E2E (manual) | docker-compose | 3 | RP-04, RD-07 |
| US-10 | Pipeline CI | ✅ 6/6 | CI (observacional) | `.github/workflows/ci.yml` | 3 | RP-03, RD-09 |

### 9.2 Validación INVEST como Garantía de Testabilidad

El principio **T (Testable)** de INVEST exige que cada historia tenga criterios de aceptación observables. En este proyecto:

- **Todas las historias** tienen escenarios Gherkin (`Given/When/Then`) que definen estados verificables.
- Los escenarios se traducen directamente a assertions en pytest:
  - `Then el sistema responde con código 201` → `self.assertEqual(response.status_code, 201)`
  - `And se publica un evento "assignment.created"` → `mock_publisher.publish.assert_called_once()`
  - `Then no se crea un registro duplicado` → `self.assertEqual(TicketAssignment.objects.count(), 1)`

- **I (Independiente)** permite ejecutar tests de cada US en aislamiento.
- **S (Small)** mantiene cada clase de test enfocada y rápida.

---

## 10. Criterios de Entrada y Salida

### 10.1 Criterios de Entrada (para iniciar pruebas)

| # | Criterio | Verificación |
|---|----------|-------------|
| 1 | User Stories definidas y validadas (INVEST ✅ 6/6) | Documento `USERSTORIES Y CRITERIOS DE ACEPTACION.md` aprobado |
| 2 | Código fuente completo y compilable | `pip install -r requirements.txt` sin errores |
| 3 | Base de datos de test disponible | `python manage.py migrate --noinput` exitoso |
| 4 | CI pipeline configurado y funcional | Push a rama trigger workflow en GH Actions |
| 5 | Entorno Docker operativo | `docker-compose up -d` levanta todos los servicios |

### 10.2 Criterios de Salida (para dar por completadas las pruebas)

| # | Criterio | Umbral |
|---|----------|--------|
| 1 | Todos los tests unitarios pasan | 100% pass rate |
| 2 | Todos los tests de integración pasan | 100% pass rate |
| 3 | Cobertura global de código | ≥ 70% |
| 4 | Cobertura de capa de dominio | ≥ 90% |
| 5 | Zero tests flaky en CI (últimas 3 ejecuciones) | 0 flaky tests |
| 6 | Pipeline CI en verde para rama `main` | Status: ✅ passing |
| 7 | Flujos E2E ejecutados al menos 1 vez en Docker | Evidencia documentada |
| 8 | Riesgos de producto (Alto impacto) mitigados | Todos con tests asociados |
| 9 | Linting sin errores (flake8) | 0 violations |

---

## 11. Roles y Responsabilidades

| Rol | Responsabilidad en Testing |
|-----|---------------------------|
| **Desarrollador** | Escribir tests unitarios y de integración; mantener cobertura ≥ 70%; corregir defectos |
| **QA / Tester** | Ejecutar pruebas E2E con Postman; verificar escenarios Gherkin manualmente; reportar bugs |
| **DevOps** | Mantener CI pipeline; configurar service containers (PostgreSQL); gestionar Docker |
| **Líder Técnico** | Revisar plan de pruebas; aprobar criterios de salida; sign-off final de calidad |
| **Product Owner** | Validar que los escenarios Gherkin reflejan el comportamiento esperado de negocio |

---

## Apéndice A — Comandos de Ejecución

### Tests Unitarios + Integración (sin Docker)

```bash
# Ejecutar toda la suite (excepto E2E que requiere broker real)
pytest --cov=assignments --cov=messaging --cov-report=term-missing -v

# Solo tests de dominio (más rápidos)
pytest assignments/tests/test_assignments.py -k "AssignmentEntity or DomainEvents" -v

# Con umbral de cobertura
pytest --cov=assignments --cov=messaging --cov-fail-under=70 -v
```

### Tests E2E (requiere Docker)

```bash
# Levantar ecosistema completo
docker-compose up -d

# Ejecutar tests de integración E2E
docker-compose exec backend pytest assignments/test_integration.py -v

# Tests de reconexión y DLQ
docker-compose exec backend pytest messaging/test_consumer_reconnection.py messaging/test_dead_letter_queue.py -v
```

### CI Pipeline (automático en GH Actions)

```bash
# Reproducir localmente lo que ejecuta CI
pytest \
  --cov=assignments \
  --cov=messaging \
  --cov-report=term-missing \
  --cov-report=xml:coverage.xml \
  --cov-fail-under=70 \
  --ignore=assignments/test_integration.py \
  --ignore=assignments/tests.py \
  -k "not AssignmentIntegrationTests" \
  -v
```

### Linting

```bash
flake8 assignments/ messaging/ assessment_service/ --count --show-source --statistics
```

---

> **Documento generado como parte del Taller Semana 3 — Actividad 3.3**  
> Referencia cruzada: [USERSTORIES Y CRITERIOS DE ACEPTACION.md](USERSTORIES%20Y%20CRITERIOS%20DE%20ACEPTACION.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [ci.yml](.github/workflows/ci.yml)
