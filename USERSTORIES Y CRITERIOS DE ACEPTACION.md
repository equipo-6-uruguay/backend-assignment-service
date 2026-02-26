# USER STORIES Y CRITERIOS DE ACEPTACIÓN

## 📋 Contexto de Negocio

El **assignment-service** es un microservicio Django construido con arquitectura DDD (Domain-Driven Design) y Event-Driven Architecture (EDA). Su responsabilidad es gestionar la asignación de tickets a agentes de soporte dentro de un ecosistema de microservicios.

El servicio:
- Expone una **API REST** para operaciones CRUD y acciones especializadas sobre asignaciones.
- **Consume eventos** (`ticket.created`, `ticket.priority_changed`) publicados por el `ticket-service` a través de RabbitMQ.
- **Publica eventos de dominio** (`assignment.created`, `assignment.reassigned`) para notificar a otros servicios del ecosistema.
- Mantiene su propia base de datos **PostgreSQL** (independiente del ticket-service).
- Procesa mensajes de forma asíncrona mediante **Celery** y cuenta con **Dead Letter Queue** para mensajes fallidos.

---

## 🎯 Objetivos del Producto

1. Exponer una API REST semánticamente correcta (verbos HTTP y códigos de estado) para la gestión de asignaciones de tickets.
2. Consumir eventos del ecosistema (`ticket.created`, `ticket.priority_changed`) y reaccionar creando o actualizando asignaciones automáticamente.
3. Publicar eventos de dominio (`assignment.created`, `assignment.reassigned`) para mantener la coherencia eventual entre microservicios.
4. Garantizar portabilidad y despliegue reproducible mediante contenerización con Docker y Docker Compose.
5. Asegurar calidad continua con pruebas automatizadas en pipeline CI (GitHub Actions) con cobertura mínima del 70%.

---

## 📦 Épicas

| Épica | Descripción de Valor |
|-------|---------------------|
| **EP-01: API REST de Asignaciones** | Permitir a los consumidores del servicio crear, consultar, modificar y eliminar asignaciones a través de endpoints RESTful. |
| **EP-02: Procesamiento de Eventos** | Integrar el servicio con el ecosistema de microservicios consumiendo y publicando eventos de dominio vía RabbitMQ. |
| **EP-03: Contenerización y Despliegue** | Garantizar portabilidad del servicio mediante Docker y orquestación con Docker Compose. |
| **EP-04: Calidad Continua (CI)** | Automatizar la validación de calidad con un pipeline de GitHub Actions que ejecute pruebas y exija cobertura mínima. |

---

# 📝 Historias de Usuario

---

## EP-01: API REST de Asignaciones

---

### US-01 — Crear una asignación de ticket vía API

**Como** agente de soporte
**quiero** crear una nueva asignación de ticket a través de la API REST
**para** registrar formalmente que un ticket ha sido asignado con una prioridad específica.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:api-rest-asignaciones @story:US-01 @priority:alta @risk:medio
Feature: Crear asignación de ticket vía API
  Como agente de soporte
  Quiero crear una nueva asignación de ticket
  Para registrar formalmente la asignación con prioridad

  Scenario: Creación exitosa de asignación con datos válidos
    Given el sistema está operativo y la base de datos accesible
    And no existe una asignación previa para el ticket "TK-100"
    When envío una petición POST a "/assignments/" con body {"ticket_id": "TK-100", "priority": "high"}
    Then el sistema responde con código de estado 201 Created
    And el cuerpo de respuesta contiene el campo "id" con un valor numérico
    And el campo "ticket_id" es "TK-100"
    And el campo "priority" es "high"
    And el campo "assigned_at" contiene una fecha ISO válida

  Scenario: Creación idempotente cuando ya existe asignación para el ticket
    Given existe una asignación para el ticket "TK-100" con prioridad "high"
    When envío una petición POST a "/assignments/" con body {"ticket_id": "TK-100", "priority": "medium"}
    Then el sistema responde con código de estado 201 Created
    And la asignación retornada mantiene la prioridad original "high"
    And no se crea un registro duplicado en la base de datos

  Scenario: Rechazo por prioridad inválida
    Given el sistema está operativo
    When envío una petición POST a "/assignments/" con body {"ticket_id": "TK-101", "priority": "critical"}
    Then el sistema responde con código de estado 400 Bad Request
    And el cuerpo contiene un mensaje de error indicando las prioridades válidas

  Scenario: Rechazo por ticket_id vacío
    Given el sistema está operativo
    When envío una petición POST a "/assignments/" con body {"ticket_id": "", "priority": "low"}
    Then el sistema responde con código de estado 400 Bad Request
    And el cuerpo contiene un mensaje de error indicando que "ticket_id" es requerido
```

### Notas

- **Valor de negocio:** Permite el registro formal de asignaciones, habilitando trazabilidad completa del ciclo de vida del ticket.
- **Supuestos confirmados:** Las prioridades válidas son `high`, `medium`, `low` y `unassigned`. La idempotencia se aplica por `ticket_id`.
- **Dependencias:** Requiere que el `ticket-service` publique IDs de ticket válidos.

### Validación INVEST

```
✅ INVEST — US-01: Crear asignación de ticket vía API
I: ✅ Se puede implementar y desplegar sin depender de otras historias del backlog.
N: ✅ Describe intención de negocio (registrar asignación); la implementación (endpoint, serializer) es negociable.
V: ✅ Valor explícito: trazabilidad formal de asignaciones de tickets.
E: ✅ Alcance claro: un endpoint POST con validaciones definidas y prioridades conocidas.
S: ✅ Cabe en un sprint; es un solo endpoint con lógica de creación y validación.
T: ✅ Criterios Gherkin observables con 4 escenarios verificables por Postman o pytest.
```

---

### US-02 — Consultar todas las asignaciones

**Como** supervisor del equipo de soporte
**quiero** consultar la lista completa de asignaciones de tickets
**para** tener visibilidad del estado actual de la distribución de trabajo.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:api-rest-asignaciones @story:US-02 @priority:alta @risk:bajo
Feature: Consultar lista de asignaciones
  Como supervisor del equipo de soporte
  Quiero consultar todas las asignaciones
  Para tener visibilidad de la distribución de trabajo

  Scenario: Listado exitoso con asignaciones existentes
    Given existen 3 asignaciones registradas en el sistema
    When envío una petición GET a "/assignments/"
    Then el sistema responde con código de estado 200 OK
    And el cuerpo contiene un arreglo con 3 elementos
    And cada elemento tiene los campos "id", "ticket_id", "priority", "assigned_at" y "assigned_to"

  Scenario: Listado vacío cuando no hay asignaciones
    Given no existen asignaciones registradas en el sistema
    When envío una petición GET a "/assignments/"
    Then el sistema responde con código de estado 200 OK
    And el cuerpo contiene un arreglo vacío

  Scenario: Las asignaciones se ordenan por fecha más reciente primero
    Given existen asignaciones creadas en orden: "TK-001" (hace 2 horas), "TK-002" (hace 1 hora), "TK-003" (hace 5 minutos)
    When envío una petición GET a "/assignments/"
    Then el primer elemento del arreglo corresponde al ticket "TK-003"
    And el último elemento corresponde al ticket "TK-001"
```

### Notas

- **Valor de negocio:** Visibilidad operativa para supervisores sobre la carga de trabajo asignada.
- **Supuestos confirmados:** El ordenamiento es por `assigned_at` descendente (más reciente primero).
- **Dependencias:** Ninguna directa.

### Validación INVEST

```
✅ INVEST — US-02: Consultar todas las asignaciones
I: ✅ Independiente; el GET no depende del POST para su implementación (puede usar fixtures).
N: ✅ Describe intención de consulta; formato de respuesta y paginación son negociables.
V: ✅ Visibilidad operativa para supervisores.
E: ✅ Alcance mínimo: un endpoint GET que retorna lista serializada.
S: ✅ Muy pequeña; lectura directa del repositorio.
T: ✅ 3 escenarios verificables con datos de prueba controlados.
```

---

### US-03 — Consultar una asignación específica por ID

**Como** agente de soporte
**quiero** consultar los detalles de una asignación específica por su ID
**para** verificar la prioridad, el ticket asociado y el usuario asignado.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:api-rest-asignaciones @story:US-03 @priority:media @risk:bajo
Feature: Consultar asignación por ID
  Como agente de soporte
  Quiero consultar una asignación específica
  Para verificar sus detalles

  Scenario: Consulta exitosa de asignación existente
    Given existe una asignación con ID 1 para el ticket "TK-200" con prioridad "medium"
    When envío una petición GET a "/assignments/1/"
    Then el sistema responde con código de estado 200 OK
    And el cuerpo contiene "ticket_id" igual a "TK-200"
    And el cuerpo contiene "priority" igual a "medium"

  Scenario: Consulta de asignación inexistente
    Given no existe una asignación con ID 999
    When envío una petición GET a "/assignments/999/"
    Then el sistema responde con código de estado 404 Not Found

  Scenario: Consulta incluye campo assigned_to cuando está asignado a un usuario
    Given existe una asignación con ID 2 asignada al usuario "agent-42"
    When envío una petición GET a "/assignments/2/"
    Then el sistema responde con código de estado 200 OK
    And el campo "assigned_to" es "agent-42"
```

### Notas

- **Valor de negocio:** Permite verificación puntual de asignaciones por parte de agentes y supervisores.
- **Supuestos confirmados:** El endpoint usa el ID numérico interno de la asignación, no el `ticket_id`.
- **Dependencias:** Ninguna directa.

### Validación INVEST

```
✅ INVEST — US-03: Consultar asignación por ID
I: ✅ Independiente; consulta por clave primaria sin dependencias funcionales.
N: ✅ Intención de negocio clara; estructura de respuesta negociable.
V: ✅ Permite a agentes verificar estado de asignaciones puntuales.
E: ✅ Alcance mínimo: un endpoint GET con parámetro de ruta.
S: ✅ Muy pequeña.
T: ✅ 3 escenarios observables con respuestas HTTP verificables.
```

---

### US-04 — Reasignar la prioridad de un ticket

**Como** supervisor del equipo de soporte
**quiero** cambiar la prioridad de una asignación existente
**para** ajustar la urgencia de atención de un ticket según la evolución del incidente.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:api-rest-asignaciones @story:US-04 @priority:alta @risk:medio
Feature: Reasignar prioridad de ticket
  Como supervisor del equipo de soporte
  Quiero cambiar la prioridad de una asignación existente
  Para ajustar la urgencia según la evolución del incidente

  Scenario: Reasignación exitosa de prioridad
    Given existe una asignación para el ticket "TK-300" con prioridad "low"
    When envío una petición POST a "/assignments/reassign/" con body {"ticket_id": "TK-300", "priority": "high"}
    Then el sistema responde con código de estado 200 OK
    And el campo "priority" es "high"
    And se publica un evento "assignment.reassigned" con old_priority "low" y new_priority "high"

  Scenario: Reasignación con la misma prioridad actual (sin cambios)
    Given existe una asignación para el ticket "TK-300" con prioridad "high"
    When envío una petición POST a "/assignments/reassign/" con body {"ticket_id": "TK-300", "priority": "high"}
    Then el sistema responde con código de estado 200 OK
    And la prioridad sigue siendo "high"
    And no se publica un evento de reasignación

  Scenario: Reasignación de ticket sin asignación previa
    Given no existe asignación para el ticket "TK-999"
    When envío una petición POST a "/assignments/reassign/" con body {"ticket_id": "TK-999", "priority": "medium"}
    Then el sistema responde con código de estado 400 Bad Request
    And el cuerpo contiene un mensaje indicando que no existe asignación para el ticket

  Scenario: Reasignación con prioridad inválida
    Given existe una asignación para el ticket "TK-300"
    When envío una petición POST a "/assignments/reassign/" con body {"ticket_id": "TK-300", "priority": "urgent"}
    Then el sistema responde con código de estado 400 Bad Request
    And el cuerpo contiene las prioridades válidas permitidas
```

### Notas

- **Valor de negocio:** Flexibilidad operativa para supervisores ante incidentes que escalan o desescalan.
- **Supuestos confirmados:** La reasignación con misma prioridad es idempotente (no genera evento). Prioridades válidas: `high`, `medium`, `low`, `unassigned`.
- **Dependencias:** Requiere que la asignación exista previamente (US-01 o evento consumido).

### Validación INVEST

```
✅ INVEST — US-04: Reasignar prioridad de un ticket
I: ✅ Independiente en implementación; la dependencia de dato (asignación existente) se resuelve con fixtures.
N: ✅ Intención de negocio clara; mecanismo de reasignación negociable (endpoint dedicado vs. PATCH).
V: ✅ Valor directo: ajuste de urgencia operativa en tiempo real.
E: ✅ Alcance delimitado: un endpoint con validación de existencia y prioridad.
S: ✅ Cabe en un sprint; un caso de uso con 2 validaciones.
T: ✅ 4 escenarios verificables incluyendo idempotencia y errores.
```

---

### US-05 — Asignar o reasignar un usuario a una asignación

**Como** supervisor del equipo de soporte
**quiero** asignar o cambiar el agente responsable de una asignación
**para** distribuir la carga de trabajo de manera equitativa y dirigir tickets a los agentes más adecuados.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:api-rest-asignaciones @story:US-05 @priority:alta @risk:medio
Feature: Asignar usuario a asignación
  Como supervisor del equipo de soporte
  Quiero asignar o cambiar el agente responsable
  Para distribuir la carga de trabajo equitativamente

  Scenario: Asignación exitosa de usuario a una asignación existente
    Given existe una asignación con ID 5 sin usuario asignado
    When envío una petición PATCH a "/assignments/5/assign-user/" con body {"assigned_to": "agent-15"}
    Then el sistema responde con código de estado 200 OK
    And el campo "assigned_to" es "agent-15"

  Scenario: Reasignación de usuario en asignación que ya tenía agente
    Given existe una asignación con ID 5 asignada al usuario "agent-10"
    When envío una petición PATCH a "/assignments/5/assign-user/" con body {"assigned_to": "agent-20"}
    Then el sistema responde con código de estado 200 OK
    And el campo "assigned_to" es "agent-20"

  Scenario: Desasignación de usuario (liberar asignación)
    Given existe una asignación con ID 5 asignada al usuario "agent-10"
    When envío una petición PATCH a "/assignments/5/assign-user/" con body {"assigned_to": null}
    Then el sistema responde con código de estado 200 OK
    And el campo "assigned_to" es null

  Scenario: Intento de asignar usuario a asignación inexistente
    Given no existe una asignación con ID 999
    When envío una petición PATCH a "/assignments/999/assign-user/" con body {"assigned_to": "agent-15"}
    Then el sistema responde con código de estado 400 Bad Request
    And el cuerpo contiene un mensaje indicando que no existe la asignación
```

### Notas

- **Valor de negocio:** Control directo sobre distribución de trabajo; permite balanceo de carga manual por supervisores.
- **Supuestos confirmados:** `assigned_to` es una referencia lógica (string) al servicio de usuarios, sin foreign key. Enviar `null` desasigna al usuario.
- **Dependencias:** El ID de usuario debe ser válido en el servicio de usuarios (validación eventual, no sincrónica).

### Validación INVEST

```
✅ INVEST — US-05: Asignar o reasignar usuario
I: ✅ Independiente; no requiere que la reasignación de prioridad exista.
N: ✅ Intención clara; se podría implementar con PUT, PATCH, o acción custom.
V: ✅ Control operativo directo de distribución de trabajo.
E: ✅ Alcance claro: un endpoint PATCH con 3 variantes (asignar, reasignar, desasignar).
S: ✅ Cabe en un sprint; caso de uso sencillo.
T: ✅ 4 escenarios con resultados observables vía respuesta HTTP.
```

---

### US-06 — Eliminar una asignación

**Como** supervisor del equipo de soporte
**quiero** eliminar una asignación que ya no es válida
**para** mantener limpio el registro de asignaciones activas y evitar confusión operativa.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:api-rest-asignaciones @story:US-06 @priority:media @risk:bajo
Feature: Eliminar asignación
  Como supervisor del equipo de soporte
  Quiero eliminar una asignación inválida
  Para mantener limpio el registro de asignaciones activas

  Scenario: Eliminación exitosa de asignación existente
    Given existe una asignación con ID 7
    When envío una petición DELETE a "/assignments/7/"
    Then el sistema responde con código de estado 204 No Content
    And la asignación con ID 7 ya no existe en la base de datos

  Scenario: Intento de eliminar asignación inexistente
    Given no existe una asignación con ID 888
    When envío una petición DELETE a "/assignments/888/"
    Then el sistema responde con código de estado 404 Not Found

  Scenario: Verificación post-eliminación
    Given existía una asignación con ID 7 que fue eliminada
    When envío una petición GET a "/assignments/7/"
    Then el sistema responde con código de estado 404 Not Found
```

### Notas

- **Valor de negocio:** Higiene operativa del backlog de asignaciones.
- **Supuestos confirmados:** La eliminación es irreversible (hard delete) mediante el `ModelViewSet` de DRF.
- **Dependencias:** Ninguna directa.

### Validación INVEST

```
✅ INVEST — US-06: Eliminar asignación
I: ✅ Completamente independiente.
N: ✅ Se podría negociar soft delete vs hard delete.
V: ✅ Limpieza operativa del registro.
E: ✅ Un endpoint DELETE estándar.
S: ✅ Mínima; provista por defecto por ModelViewSet.
T: ✅ 3 escenarios verificables con peticiones HTTP.
```

---

## EP-02: Procesamiento de Eventos

---

### US-07 — Crear asignación automáticamente al recibir evento de ticket creado

**Como** sistema de asignaciones
**quiero** crear automáticamente una asignación cuando se recibe un evento `ticket.created` desde RabbitMQ
**para** garantizar que todo ticket nuevo tenga una asignación registrada sin intervención manual.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:procesamiento-eventos @story:US-07 @priority:alta @risk:alto
Feature: Creación automática de asignación por evento ticket.created
  Como sistema de asignaciones
  Quiero crear asignaciones al recibir eventos de ticket
  Para garantizar asignación automática sin intervención manual

  Background:
    Given el consumidor RabbitMQ está conectado al exchange del ticket-service
    And la cola de asignaciones está declarada y vinculada

  Scenario: Asignación creada al recibir evento ticket.created
    Given no existe asignación para el ticket "TK-500"
    When se recibe un mensaje con event_type "ticket.created" y ticket_id "TK-500" y priority "medium"
    Then se crea una asignación para el ticket "TK-500" con prioridad "medium"
    And se publica un evento "assignment.created" al exchange de asignaciones

  Scenario: Evento duplicado no genera asignación duplicada (idempotencia)
    Given ya existe una asignación para el ticket "TK-500"
    When se recibe nuevamente un mensaje con event_type "ticket.created" y ticket_id "TK-500"
    Then no se crea una nueva asignación
    And la asignación existente se mantiene sin cambios

  Scenario: Mensaje malformado se envía a Dead Letter Queue
    Given se recibe un mensaje con JSON inválido o campos faltantes
    When el handler intenta procesar el mensaje
    Then el mensaje es rechazado con basic_nack sin requeue
    And el mensaje es enrutado a la Dead Letter Queue para inspección
```

### Notas

- **Valor de negocio:** Automatiza completamente el flujo de asignación, eliminando el riesgo de tickets huérfanos.
- **Supuestos confirmados:** El procesamiento se delega a Celery (`process_ticket_event.delay`). La DLQ captura mensajes fallidos.
- **Dependencias:** Requiere que el `ticket-service` publique eventos en formato esperado y RabbitMQ esté disponible.

### Validación INVEST

```
✅ INVEST — US-07: Creación automática por evento
I: ✅ Independiente del API REST; se prueba con mensajes directos a la cola.
N: ✅ El mecanismo (Celery, síncrono) es negociable; la intención (asignación automática) es fija.
V: ✅ Automatización clave del flujo de negocio.
E: ✅ Alcance claro: consumir mensaje → crear asignación → publicar evento.
S: ✅ Un handler con lógica delegada a caso de uso existente.
T: ✅ 3 escenarios con estados verificables en BD y cola.
```

---

### US-08 — Actualizar prioridad de asignación al recibir evento de cambio de prioridad del ticket

**Como** sistema de asignaciones
**quiero** actualizar automáticamente la prioridad de una asignación cuando se recibe el evento `ticket.priority_changed`
**para** mantener la coherencia de prioridades entre tickets y asignaciones sin intervención manual.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:procesamiento-eventos @story:US-08 @priority:alta @risk:medio
Feature: Actualización automática de prioridad por evento
  Como sistema de asignaciones
  Quiero actualizar la prioridad al recibir ticket.priority_changed
  Para mantener coherencia entre tickets y asignaciones

  Background:
    Given el consumidor RabbitMQ está activo y procesando mensajes

  Scenario: Prioridad actualizada al recibir evento de cambio
    Given existe una asignación para el ticket "TK-600" con prioridad "low"
    When se recibe un evento "ticket.priority_changed" con ticket_id "TK-600" y new_priority "high"
    Then la asignación del ticket "TK-600" se actualiza a prioridad "high"

  Scenario: Evento de cambio para ticket sin asignación no genera error
    Given no existe asignación para el ticket "TK-700"
    When se recibe un evento "ticket.priority_changed" con ticket_id "TK-700" y new_priority "medium"
    Then el sistema procesa el evento sin error
    And no se crea ninguna asignación nueva

  Scenario: Evento con prioridad inválida es rechazado
    Given existe una asignación para el ticket "TK-600"
    When se recibe un evento "ticket.priority_changed" con new_priority "critical"
    Then el sistema registra un error de validación de dominio
    And la prioridad de la asignación no cambia
```

### Notas

- **Valor de negocio:** Consistencia eventual garantizada entre servicios sin acoplamiento directo.
- **Supuestos confirmados:** Si no existe asignación para el ticket, el caso de uso retorna `None` sin error (tolerancia a eventos desconocidos).
- **Dependencias:** Requiere que `ticket-service` publique `ticket.priority_changed` con campos `ticket_id` y `new_priority`.

### Validación INVEST

```
✅ INVEST — US-08: Actualización de prioridad por evento
I: ✅ Independiente de la reasignación manual (US-04); actúa por canal de eventos.
N: ✅ Intención clara; estrategia de manejo de prioridad inválida es negociable.
V: ✅ Consistencia de datos entre microservicios.
E: ✅ Un handler + un caso de uso con 3 caminos definidos.
S: ✅ Cabe en un sprint.
T: ✅ 3 escenarios verificables con mensajes controlados.
```

---

## EP-03: Contenerización y Despliegue

---

### US-09 — Contenerizar el servicio de asignaciones con Docker

**Como** ingeniero de DevOps
**quiero** construir y ejecutar el assignment-service como un contenedor Docker
**para** garantizar portabilidad y reproducibilidad del entorno en cualquier máquina o servidor.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:contenerizacion @story:US-09 @priority:alta @risk:medio
Feature: Contenerización del servicio con Docker
  Como ingeniero de DevOps
  Quiero ejecutar el servicio como contenedor Docker
  Para garantizar portabilidad y reproducibilidad

  Scenario: Construcción exitosa de la imagen Docker
    Given existe un Dockerfile válido en la raíz del proyecto
    When ejecuto "docker build -t assignment-service ."
    Then la imagen se construye sin errores
    And la imagen resultante contiene las dependencias de requirements.txt

  Scenario: Ecosistema completo con docker-compose
    Given existen los archivos Dockerfile y docker-compose.yml en la raíz
    When ejecuto "docker-compose up -d"
    Then se levantan los servicios: API, base de datos PostgreSQL y RabbitMQ
    And el servicio de API responde en el puerto configurado
    And la base de datos acepta conexiones

  Scenario: Persistencia de datos tras reinicio de contenedores
    Given el ecosistema está corriendo con docker-compose
    And se han creado asignaciones a través de la API
    When ejecuto "docker-compose down" seguido de "docker-compose up -d"
    Then las asignaciones creadas previamente siguen disponibles
    And los datos no se pierden gracias a los volúmenes configurados
```

### Notas

- **Valor de negocio:** Elimina el problema "funciona en mi máquina"; permite despliegue en cualquier entorno.
- **Supuestos confirmados:** Se usa PostgreSQL como base de datos y RabbitMQ como broker de mensajes. Los volúmenes persisten datos de PostgreSQL.
- **Dependencias:** Requiere Docker y Docker Compose instalados en el entorno de ejecución.

### Validación INVEST

```
✅ INVEST — US-09: Contenerización con Docker
I: ✅ Independiente del código funcional; es infraestructura.
N: ✅ Imagen base, puertos y configuración son negociables.
V: ✅ Portabilidad y reproducibilidad del entorno.
E: ✅ Alcance definido: Dockerfile + docker-compose.yml + volúmenes.
S: ✅ Cabe en un sprint; configuración de 3 archivos.
T: ✅ 3 escenarios verificables ejecutando comandos Docker.
```

---

## EP-04: Calidad Continua (CI)

---

### US-10 — Pipeline de Integración Continua con GitHub Actions

**Como** líder técnico del equipo
**quiero** que se ejecuten automáticamente las pruebas del servicio con cada push o pull request
**para** detectar regresiones de forma inmediata e impedir la integración de código que rompa las pruebas existentes.

### Criterios de Aceptación (Gherkin)

```gherkin
@epic:calidad-continua @story:US-10 @priority:alta @risk:alto
Feature: Pipeline CI con GitHub Actions
  Como líder técnico del equipo
  Quiero ejecución automática de pruebas en cada push/PR
  Para detectar regresiones e impedir integración de código roto

  Scenario: Pipeline se dispara automáticamente con push a cualquier rama
    Given existe el archivo ".github/workflows/ci.yml" en el repositorio
    When un desarrollador hace push a la rama "feature/nueva-funcionalidad"
    Then el pipeline de GitHub Actions se dispara automáticamente
    And construye el entorno del servicio
    And ejecuta todas las pruebas unitarias e integración

  Scenario: Pipeline bloquea integración si alguna prueba falla
    Given el pipeline se ha disparado por un pull request hacia "develop"
    When una prueba unitaria falla durante la ejecución
    Then el pipeline reporta estado "failed" en rojo
    And el pull request queda bloqueado para merge
    And se muestra el detalle de la prueba que falló

  Scenario: Pipeline reporta cobertura de código
    Given el pipeline se ejecuta exitosamente
    When todas las pruebas pasan
    Then el reporte de cobertura muestra un porcentaje igual o superior al 70%
    And el pipeline finaliza con estado "success" en verde
```

### Notas

- **Valor de negocio:** Calidad garantizada en cada integración; prevención automática de regresiones.
- **Supuestos confirmados:** El pipeline debe dispararse en push y PR a todas las ramas (`main`, `develop`, `feature/**`). Cobertura mínima exigida: 70%.
- **Dependencias:** Requiere que las pruebas del Taller 2 estén funcionales y que GitHub Actions esté habilitado en el repositorio.

### Validación INVEST

```
✅ INVEST — US-10: Pipeline CI con GitHub Actions
I: ✅ Independiente del código funcional; es configuración de infraestructura CI.
N: ✅ Herramienta (Actions), umbrales y triggers son negociables.
V: ✅ Protección automática contra regresiones.
E: ✅ Alcance claro: un archivo YAML con etapas de build, test y coverage.
S: ✅ Cabe en un sprint; configuración de un workflow.
T: ✅ 3 escenarios verificables directamente en la pestaña Actions de GitHub.
```

---

## Resumen de Historias

| ID | Historia | Épica | Prioridad | Riesgo | INVEST |
|----|----------|-------|-----------|--------|--------|
| US-01 | Crear asignación de ticket vía API | EP-01 | Alta | Medio | ✅ 6/6 |
| US-02 | Consultar todas las asignaciones | EP-01 | Alta | Bajo | ✅ 6/6 |
| US-03 | Consultar asignación por ID | EP-01 | Media | Bajo | ✅ 6/6 |
| US-04 | Reasignar prioridad de ticket | EP-01 | Alta | Medio | ✅ 6/6 |
| US-05 | Asignar o reasignar usuario | EP-01 | Alta | Medio | ✅ 6/6 |
| US-06 | Eliminar asignación | EP-01 | Media | Bajo | ✅ 6/6 |
| US-07 | Creación automática por evento ticket.created | EP-02 | Alta | Alto | ✅ 6/6 |
| US-08 | Actualización de prioridad por evento | EP-02 | Alta | Medio | ✅ 6/6 |
| US-09 | Contenerización con Docker | EP-03 | Alta | Medio | ✅ 6/6 |
| US-10 | Pipeline CI con GitHub Actions | EP-04 | Alta | Alto | ✅ 6/6 |