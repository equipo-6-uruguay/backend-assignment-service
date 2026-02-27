# DOLORES.md — Auditoría de Deuda Técnica del Monolito

**Proyecto:** Assignment Service (Django + DDD + EDA)  
**Fecha:** 24 de Febrero, 2026  
**Versión:** 1.0  
**Equipo:** Equipo 6 Uruguay

---

## 1. Resumen Ejecutivo

Este documento cataloga de forma exhaustiva los "dolores" (problemas técnicos, arquitectónicos y de calidad) identificados en el código base actual del monolito heredado. El objetivo es visibilizar la deuda técnica acumulada para priorizar la refactorización hacia una **Clean Architecture** (Robert C. Martin).

Se identificaron **10+ hallazgos activos** distribuidos en 10 categorías, con **4 de severidad alta** y **6 de severidad media**.

### Estado de trazabilidad (2026-02-27)

- Este archivo mantiene **solo dolores activos** en `develop`.
- Los dolores resueltos se registran en `DOLORES_RESUELTOS.md`.
- Revisión de GitHub al 2026-02-27: **2 PRs mergeadas** (#2, #4) y **4 PRs abiertas** (#6, #8, #14, #16).
- Resultado: se migraron a resueltos **CFG-01, SEC-01, SEC-02, NOM-01, NOM-02, TST-02, SCL-01, DOC-01, EDA-01, EDA-02, ERR-02, CPL-01, CPL-02**.
- Nota operativa: los cambios de PR abierta (por ejemplo #8 sobre limpieza de tests/docs) **no** se consideran resueltos hasta merge en rama objetivo.

### Top 5 Problemas Críticos

| # | Dolor | Categoría | Impacto |
|---|---|---|---|
| 1 | Archivo de tests tipo "god file" con mezcla de capas | Modularidad | Alto costo de mantenimiento y baja confiabilidad de suite |
| 2 | ViewSet acoplado a infraestructura concreta | Acoplamiento | Imposibilidad de sustituir adaptadores o testear aisladamente |
| 3 | Repository update sin manejo de `DoesNotExist` | Manejo de Errores | Error 500 no controlado ante IDs huérfanos |
| 4 | Reconexión en consumer atrapa cualquier error inesperado | Manejo de Errores | Fiabilidad, deuda técnica |
| 5 | Conexión RabbitMQ nueva por cada evento publicado | Escalabilidad | Reduce throughput del sistema de mensajería |

---

## 2. Metodología de Auditoría

La auditoría se realizó mediante **análisis estático** y **revisión manual** del código fuente, evaluando los siguientes criterios:

| Criterio | Descripción |
|---|---|
| Principios SOLID | Verificación de SRP, OCP, DIP, ISP en todas las capas |
| Clean Architecture | Evaluación de la Dependency Rule y separación de capas |
| Seguridad | Credenciales, validación de entrada, configuración de host |
| Resiliencia EDA | Reintentos, idempotencia, ACK/NACK, Dead Letter Queues |
| Escalabilidad | Paginación, conexiones, queries |
| Cobertura de pruebas | Calidad, consistencia y cobertura real de tests |
| Clean Code | Nomenclatura, imports, documentación |

### Escala de Severidad

| Icono | Nivel | Definición |
|---|---|---|
| 🔴 | **Alta** | Causa fallos críticos, brechas de seguridad o impide la evolución del sistema |
| 🟡 | **Media** | Afecta mantenibilidad o rendimiento; debe planificarse su corrección |
| 🟢 | **Baja** | Problemas cosméticos o de estilo que no afectan funcionalidad |

---

## 3. Mapa de Cobertura de Archivos

Archivos analizados durante esta auditoría:

### Configuración del Proyecto
- [x] `manage.py`
- [x] `assessment_service/settings.py`
- [x] `assessment_service/urls.py`
- [x] `assessment_service/celery.py`
- [x] `Dockerfile`
- [x] `docker-compose.yml`
- [x] `requirements.txt`

### Capa de Presentación
- [x] `assignments/views.py`
- [x] `assignments/serializers.py`
- [x] `assignments/urls.py`

### Capa de Dominio
- [x] `assignments/domain/entities.py`
- [x] `assignments/domain/events.py`
- [x] `assignments/domain/repository.py`

### Capa de Aplicación
- [x] `assignments/application/event_publisher.py`
- [x] `assignments/application/use_cases/create_assignment.py`
- [x] `assignments/application/use_cases/reassign_ticket.py`
- [x] `assignments/application/use_cases/change_assignment_priority.py`
- [x] `assignments/application/use_cases/update_assigned_user.py`

### Capa de Infraestructura
- [x] `assignments/infrastructure/django_models.py`
- [x] `assignments/infrastructure/repository.py`
- [x] `assignments/infrastructure/cookie_auth.py`
- [x] `assignments/infrastructure/messaging/event_publisher.py`
- [x] `assignments/infrastructure/messaging/event_adapter.py`

### Mensajería
- [x] `messaging/consumer.py`
- [x] `messaging/handlers.py`

### Pruebas
- [x] `assignments/tests.py`
- [x] `assignments/test_integration.py`
- [x] `assignments/tests/test_cors_middleware_order.py`
- [x] `messaging/test_consumer_reconnection.py`
- [x] `messaging/test_dead_letter_queue.py`

---

## 4. Catálogo Detallado de Dolores

### 4.1. Acoplamiento Fuerte

#### [CPL-01] ViewSet acoplado a infraestructura concreta (sin inversión de dependencias)

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #11 / PR #12, rama `feature/composition-root-di`).

---

#### [CPL-02] Handler de mensajería crea dependencias concretas por evento

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #11 / PR #12, rama `feature/composition-root-di`).

---

### 4.2. Duplicación de Código

#### [DUP-01] Tests de integración E2E duplicados en múltiples archivos

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `assignments/tests.py`, `assignments/test_integration.py`, `assignments/tests/test_assignments.py` |

**Descripción:**  
Existe `AssignmentIntegrationTests` en múltiples módulos con flujo casi idéntico (RabbitMQ→consumer→DB), generando mantenimiento duplicado y riesgo de divergencia.

**Impacto:** Deuda técnica, mantenibilidad

**Evidencia:**
```python
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class AssignmentIntegrationTests(TestCase):
    def setUp(self):
        try:
            from celery import current_app
            current_app.conf.task_always_eager = True
            current_app.conf.task_eager_propagates = True
        except Exception:
```

---

### 4.3. Manejo de Errores Deficiente

#### [ERR-01] Repository update sin control de `DoesNotExist`

| **Severidad** | **Ubicación** |
|---|---|
| 🔴 Alta | `assignments/infrastructure/repository.py` (líneas 19-31) |

**Descripción:**  
En `save()`, la rama de actualización hace `get(id=assignment.id)` sin manejo de excepción. Un ID huérfano provoca un error 500 no controlado en vez de un error de dominio.

**Impacto:** Mantenibilidad, fiabilidad

**Evidencia:**
```python
def save(self, assignment: Assignment) -> Assignment:
    if assignment.id:
        model = TicketAssignmentModel.objects.get(id=assignment.id)
        model.priority = assignment.priority
        model.assigned_to = assignment.assigned_to
        model.save()
    else:
        model = TicketAssignmentModel.objects.create(
            ticket_id=assignment.ticket_id,
```

---

#### [ERR-02] `except Exception` genérico en publisher y adapter

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (PR #16; pendiente merge a `develop`).

---

#### [ERR-03] Reconexión en consumer atrapa cualquier error inesperado

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `messaging/consumer.py` (líneas 220-241) |

**Descripción:**  
El bloque global `except Exception` reintenta incluso errores de programación/configuración no transitorios, enmascarando fallos raíz.

**Impacto:** Fiabilidad, deuda técnica

**Evidencia:**
```python
except Exception as exc:
    attempt += 1
    delay = min(
        INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** attempt),
        MAX_RETRY_DELAY,
    )
    logger.error("Unexpected error (%s)...", exc, attempt, delay)
    _safe_close(connection)
    time.sleep(delay)
```

---

### 4.4. Falta de Modularidad

#### [MOD-01] Archivo de tests "god file" mezclando capas

| **Severidad** | **Ubicación** |
|---|---|
| 🔴 Alta | `assignments/tests.py` |

**Descripción:**  
Un único archivo concentra pruebas de dominio, aplicación, infraestructura, API, integración y legacy. Aunque se corrigieron errores de formato en PR #4, la concentración de responsabilidades sigue siendo una deuda estructural.

**Impacto:** Mantenibilidad, fiabilidad de pruebas

**Evidencia:**
```python
# tests.py concentra API + legacy + integración + celery en un mismo módulo
class AssignmentAPITests(APITestCase):
    ...

class LegacyAssignmentServiceTests(TestCase):
    ...

class AssignmentIntegrationTests(TestCase):
    ...
```

---

### 4.5. Valores Hardcodeados

#### [CFG-01] Credenciales RabbitMQ hardcodeadas en settings

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #1 / PR #2, rama `develop`).

---

#### [CFG-02] CMD del contenedor hardcodeado a worker Celery + migraciones

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `Dockerfile` (líneas 16-22) |

**Descripción:**  
La imagen queda fijada a un único proceso operacional. Mezcla concerns de arranque (migración) y ejecución (worker Celery) en un solo CMD.

**Impacto:** Escalabilidad, operabilidad, deuda técnica

**Evidencia:**
```dockerfile
COPY . .

EXPOSE 8001

# Comando por defecto: migrar la DB y correr worker de Celery
CMD sh -c "python manage.py migrate && celery -A assessment_service worker --loglevel=info"
```

---

### 4.6. Cobertura de Pruebas Insuficiente

#### [TST-01] Test de reconexión no prueba el módulo real, replica lógica

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `messaging/test_consumer_reconnection.py` (L1-36, L94-136) |

**Descripción:**  
Varios tests implementan bucles "simulados" replicando la lógica interna del consumer en vez de invocar directamente `start_consuming`. Pueden pasar aunque el código productivo esté roto.

**Impacto:** Fiabilidad de pruebas, deuda técnica

**Evidencia:**
```python
# Constants mirroring consumer.py defaults for isolated testing
INITIAL_RETRY_DELAY = 1
MAX_RETRY_DELAY = 60
RETRY_BACKOFF_FACTOR = 2

def _safe_close_fn(connection) -> None:
    """Mirror of consumer._safe_close for testing."""
```

---

#### [TST-02] Inconsistencia de rutas API en tests vs router real

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #3 / PR #4, mergeado).

---

### 4.7. Problemas de Escalabilidad

#### [SCL-01] Sin paginación global y queryset completo

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (PR #14; pendiente merge a `develop`).

---

#### [SCL-02] Conexión RabbitMQ nueva por cada evento publicado

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `assignments/infrastructure/messaging/event_publisher.py` (L35-68) |

**Descripción:**  
Abrir y cerrar `BlockingConnection` en cada `publish()` es costoso bajo carga y reduce el throughput del sistema de mensajería.

**Impacto:** Escalabilidad, rendimiento

**Evidencia:**
```python
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=self.host)
)
channel = connection.channel()
...
channel.basic_publish(...)
connection.close()
```

---

### 4.8. Violaciones SOLID

#### [SLD-01] Dependencia inyectada pero no utilizada en use cases

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `assignments/application/use_cases/change_assignment_priority.py` (L18-54), `assignments/application/use_cases/update_assigned_user.py` (L6-52) |

**Descripción:**  
`ChangeAssignmentPriority` y `UpdateAssignedUser` reciben `event_publisher` en su constructor pero nunca lo utilizan. Rompe coherencia OCP/DIP y el contrato implícito del pipeline EDA.

**Impacto:** Mantenibilidad, consistencia EDA

**Evidencia:**
```python
def __init__(self, repository: AssignmentRepository, event_publisher: EventPublisher):
    self.repository = repository
    self.event_publisher = event_publisher  # ← Nunca se usa
...
updated_assignment = self.repository.save(assignment)
return updated_assignment  # ← Sin publicación de evento
```

---

#### [SLD-02] Dominio usa `ValueError` genérico en lugar de excepciones de dominio

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `assignments/domain/entities.py` (líneas 24-52) |

**Descripción:**  
La entidad no define una jerarquía de excepciones específica del dominio. Usa `ValueError` genérico, lo que complica el mapeo semántico a respuestas API y dificulta el manejo diferenciado de errores.

**Impacto:** Mantenibilidad, deuda técnica

**Evidencia:**
```python
if not self.ticket_id or not self.ticket_id.strip():
    raise ValueError("ticket_id es requerido y no puede estar vacío")

if self.priority not in self.VALID_PRIORITIES:
    raise ValueError(
        f"priority debe ser uno de {self.VALID_PRIORITIES}, "
        f"recibido: {self.priority}"
    )
```

---

### 4.9. Nomenclatura Inconsistente

#### [NOM-01] Terminología incorrecta en docstring ("autoridad" vs "prioridad")

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #1 / PR #2, rama `develop`).

---

#### [NOM-02] Código muerto: `import random` no utilizado

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #1 / PR #2, rama `develop`).

---

### 4.10. Documentación Ausente

#### [DOC-01] Serializer sin validaciones explícitas del contrato de entrada

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (PR #14; pendiente merge a `develop`).

---

### 4.11. Seguridad

#### [SEC-01] `ALLOWED_HOSTS` puede quedar vacío con `DEBUG=False`

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #1 / PR #2, rama `develop`).

---

#### [SEC-02] Fallback de `CSRF_TRUSTED_ORIGINS` a localhost sin condicionar por `DEBUG`

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (Issue #1 / PR #2, rama `develop`).

---

### 4.12. Resiliencia EDA

#### [EDA-01] ACK prematuro del mensaje antes de confirmar procesamiento real

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (PR #16; pendiente merge a `develop`).

---

#### [EDA-02] Tarea Celery sin retry/backoff/autoretry explícitos

✅ **Migrado a resueltos** en `DOLORES_RESUELTOS.md` (PR #16; pendiente merge a `develop`).

---

#### [EDA-03] Inconsistencia DLQ routing key entre implementación y tests

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `messaging/consumer.py` (L48-52), `messaging/test_dead_letter_queue.py` (L30-36) |

**Descripción:**  
El consumer usa el sufijo `.dead` y los tests esperan `.dead-letter`. Esto rompe la confiabilidad del contrato operativo y puede causar mensajes perdidos en DLQ.

**Impacto:** Mantenibilidad, operabilidad

**Evidencia:**
```python
# consumer.py
DLX_SUFFIX: str = ".dlx"
DLQ_SUFFIX: str = ".dlq"
DLQ_ROUTING_KEY_SUFFIX: str = ".dead"

# test_dead_letter_queue.py espera ".dead-letter"
```

---

### 4.13. Deuda Técnica Estructural

#### [DEB-01] Inconsistencia entre migración inicial y modelo actual para `assigned_at`

| **Severidad** | **Ubicación** |
|---|---|
| 🟡 Media | `assignments/migrations/0001_initial.py` (L16-22), `assignments/infrastructure/django_models.py` (L12-18) |

**Descripción:**  
La migración inicial define `auto_now_add=True` para `assigned_at`, pero el modelo actual puede no reflejar esto consistentemente. Puede causar drift histórico/esquema inesperado entre entornos.

**Impacto:** Mantenibilidad, consistencia de datos

**Evidencia:**
```python
# Migración
('assigned_at', models.DateTimeField(auto_now_add=True)),

# Modelo actual puede diferir
```

---

## 5. Contraste: Dolores del Monolito vs Clean Architecture

**Clean Architecture** (Robert C. Martin) propone separar **políticas de negocio** (núcleo) de **detalles técnicos** (framework, DB, mensajería) aplicando la **Dependency Rule**: las dependencias siempre apuntan hacia adentro. Este contraste sirve como referencia rápida para el futuro documento `ARCHITECTURE.md`, donde se explorará a profundidad cada migración.

| Dolor Actual | Principio Clean Architecture | Beneficio Esperado | Cambio Arquitectónico Sugerido | Prioridad |
|---|---|---|---|---|
| **CPL-01/02**: Acoplamiento ViewSet y Handler a infraestructura concreta | Dependency Rule + DIP | Casos de uso independientes de Django/RabbitMQ; menor fricción al cambiar adapters | Invertir dependencias con puertos (Repository/EventPublisher) e inyección desde composición raíz | Alta |
| **CFG-02**: CMD de contenedor acoplado (migración + worker) | Frameworks & Drivers como detalle externo + SRP | Operación más portable y escalable por proceso | Separar entrypoints de runtime (web, worker, migrate) | Media |
| **SCL-02**: Conexión RabbitMQ nueva por mensaje | SRP en infraestructura + OCP | Mejor throughput, menor latencia y menor presión de red | Introducir publisher con conexión/canal reutilizable y lifecycle controlado | Media |
| **ERR-01/02/03**: Errores genéricos y sin control | SRP + DIP + manejo explícito de límites | Errores predecibles y reintentos sólo cuando corresponde | Definir taxonomía de excepciones (dominio/aplicación/infra) y políticas de retry por tipo | Alta |
| **SLD-02**: `ValueError` genérico en dominio | Modelo de dominio explícito + SRP | Reglas de negocio expresivas y trazables | Crear jerarquía de `DomainException` y mapearla en capa de aplicación | Alta |
| **EDA-03**: DLQ inconsistente (con EDA-01 y EDA-02 ya resueltos en PR #16) | Boundary control + DIP + robustez en adapters EDA | Entrega al-menos-una-vez con menor pérdida de mensajes | Mantener convención única de routing keys/DLQ y validar contrato operativo en tests/consumer | Alta |
| **DUP-01 + MOD-01**: Tests duplicados y archivo "god file" | SRP + separación por capa/caso de uso | Suites mantenibles, rápidas y con menor costo de cambio | Reorganizar tests por dominio/aplicación/infra/API y eliminar duplicados con fixtures reutilizables | Media |
| **TST-01**: Tests replican lógica del consumer en lugar de invocar el módulo real | Testabilidad real de casos de uso/adapters + OCP | Mayor confianza y menos falsos positivos | Probar comportamiento público real (módulos/routers reales), no reimplementaciones en test | Alta |
| **SLD-01**: `event_publisher` inyectado pero no usado | ISP + SRP | Contratos más pequeños y menor ruido en dependencias | Segregar interfaces y dependencias por caso de uso (solo lo que consume cada uno) | Media |
| **DEB-01**: Divergencia migración vs modelo | Single Source of Truth en límites de persistencia + SRP | Menos drift entre código y esquema; menos incidentes en deploy | Corregir contrato ORM↔migración y añadir chequeo de consistencia en CI | Alta |

---

## 6. Plan de Priorización y Remediación

> ℹ️ EDA-01, EDA-02 y ERR-02 fueron resueltos en PR #16 y migrados a `DOLORES_RESUELTOS.md`.

### ⚡ Quick Wins (Corto Plazo — 1 Sprint)

| ID | Tarea | Esfuerzo | Beneficio |
|---|---|---|---|
| — | Sin quick win nuevo pendiente tras cierre de `TST-02` | — | — |

### 🛠️ Mediano Plazo (Táctico — 2-3 Sprints)

| ID | Tarea | Esfuerzo | Beneficio |
|---|---|---|---|
| ERR-01 | Agregar manejo de `DoesNotExist` en repository update | Medio | Estabilidad |
| SLD-02 | Crear jerarquía de excepciones de dominio | Medio | Dominio expresivo |
| DUP-01 | Consolidar tests de integración duplicados | Medio | Mantenibilidad |

### 🏗️ Estructural (Largo Plazo — 3+ Sprints)

| ID | Tarea | Esfuerzo | Beneficio |
|---|---|---|---|
| CPL-01 | Implementar inversión de dependencias en ViewSet | Alto | Desacoplamiento total |
| MOD-01 | Reorganizar tests por capa (dominio/app/infra/API) | Alto | Suite mantenible |
| SCL-02 | Publisher con conexión RabbitMQ reutilizable | Alto | Throughput optimizado |
| CFG-02 | Separar entrypoints Docker (web, worker, migrate) | Alto | Operabilidad |

---

## Glosario de Severidad

| Icono | Nivel | Definición |
|---|---|---|
| 🔴 | **Alta** | Causa fallos críticos, brechas de seguridad o impide la evolución del sistema. Requiere atención inmediata. |
| 🟡 | **Media** | Afecta la mantenibilidad o rendimiento; debe planificarse su corrección. |
| 🟢 | **Baja** | Problemas cosméticos o de estilo que no afectan funcionalidad. |
