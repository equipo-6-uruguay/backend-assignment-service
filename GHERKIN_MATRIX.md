# Matriz de Ejecución de Pruebas Gherkin

**Proyecto:** backend-assignment-service (Django DDD + EDA microservice)  
**Fecha:** 2026-02-26  
**Fuente de escenarios:** [USERSTORIES Y CRITERIOS DE ACEPTACION.md](USERSTORIES%20Y%20CRITERIOS%20DE%20ACEPTACION.md)  
**Referencia de plan de pruebas:** [TEST_PLAN_V3.md](TEST_PLAN_V3.md)

## Instrucciones de Uso

- Esta matriz se utiliza para trazabilidad y seguimiento manual de ejecución de escenarios Gherkin.
- Para cada escenario ejecutado, actualizar la columna **Resultado** con uno de los siguientes valores:
  - ✅ Pasó
  - ❌ Falló
  - ⏳ Pendiente
- Registrar evidencia, incidencias o notas relevantes en la columna **Observaciones**.
- Mantener el estado inicial como **⏳ Pendiente** para escenarios no ejecutados.

## Resumen Ejecutivo

| Epic | US incluidas | Escenarios | ✅ Pasó | ❌ Falló | ⏳ Pendiente |
|---|---|---:|---:|---:|---:|
| EP-01: API REST de Asignaciones | US-01 a US-06 | 21 | 0 | 0 | 21 |
| EP-02: Procesamiento de Eventos | US-07 a US-08 | 6 | 0 | 0 | 6 |
| EP-03: Contenerización | US-09 | 3 | 0 | 0 | 3 |
| EP-04: Calidad Continua | US-10 | 3 | 0 | 0 | 3 |
| **TOTAL** | **US-01 a US-10** | **33** | **0** | **0** | **33** |

## Matriz Completa

### EP-01: API REST de Asignaciones

| ID | US | Escenario | Given | When | Then | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
| US-01-SC-01 | US-01 — Crear asignación de ticket vía API | Creación exitosa con datos válidos | el sistema está operativo y la base de datos accesible AND no existe una asignación previa para el ticket "TK-100" | envío una petición POST a "/api/assignments/" con body {"ticket_id": "TK-100", "priority": "high"} | el sistema responde con código 201 Created AND el cuerpo contiene "id" numérico, "ticket_id"="TK-100", "priority"="high", "assigned_at" ISO válida | ⏳ Pendiente | |
| US-01-SC-02 | US-01 — Crear asignación de ticket vía API | Creación idempotente cuando ya existe asignación | existe una asignación para el ticket "TK-100" con prioridad "high" | envío POST a "/api/assignments/" con body {"ticket_id": "TK-100", "priority": "medium"} | responde 201 Created AND la asignación mantiene prioridad original "high" AND no se crea duplicado | ⏳ Pendiente | |
| US-01-SC-03 | US-01 — Crear asignación de ticket vía API | Rechazo por prioridad inválida | el sistema está operativo | envío POST a "/api/assignments/" con body {"ticket_id": "TK-101", "priority": "critical"} | responde 400 Bad Request AND mensaje con prioridades válidas | ⏳ Pendiente | |
| US-01-SC-04 | US-01 — Crear asignación de ticket vía API | Rechazo por ticket_id vacío | el sistema está operativo | envío POST a "/api/assignments/" con body {"ticket_id": "", "priority": "low"} | responde 400 Bad Request AND mensaje indicando ticket_id requerido | ⏳ Pendiente | |
| US-02-SC-01 | US-02 — Consultar todas las asignaciones | Listado exitoso con asignaciones existentes | existen 3 asignaciones registradas | GET a "/api/assignments/" | 200 OK AND arreglo con 3 elementos AND cada uno tiene id, ticket_id, priority, assigned_at, assigned_to | ⏳ Pendiente | |
| US-02-SC-02 | US-02 — Consultar todas las asignaciones | Listado vacío | no existen asignaciones | GET a "/api/assignments/" | 200 OK AND arreglo vacío | ⏳ Pendiente | |
| US-02-SC-03 | US-02 — Consultar todas las asignaciones | Ordenamiento por fecha descendente | asignaciones TK-001 (2h ago), TK-002 (1h ago), TK-003 (5min ago) | GET a "/api/assignments/" | primer elemento es TK-003, último es TK-001 | ⏳ Pendiente | |
| US-03-SC-01 | US-03 — Consultar asignación por ID | Consulta exitosa | asignación ID 1, ticket "TK-200", prioridad "medium" | GET "/api/assignments/1/" | 200 OK AND ticket_id="TK-200", priority="medium" | ⏳ Pendiente | |
| US-03-SC-02 | US-03 — Consultar asignación por ID | Consulta inexistente | no existe asignación ID 999 | GET "/api/assignments/999/" | 404 Not Found | ⏳ Pendiente | |
| US-03-SC-03 | US-03 — Consultar asignación por ID | Consulta con assigned_to | asignación ID 2 asignada a "agent-42" | GET "/api/assignments/2/" | 200 OK AND assigned_to="agent-42" | ⏳ Pendiente | |
| US-04-SC-01 | US-04 — Reasignar prioridad | Reasignación exitosa | asignación TK-300 con prioridad "low" | POST "/api/assignments/reassign/" con {"ticket_id": "TK-300", "priority": "high"} | 200 OK AND priority="high" AND evento assignment.reassigned publicado | ⏳ Pendiente | |
| US-04-SC-02 | US-04 — Reasignar prioridad | Misma prioridad (idempotente) | asignación TK-300 con prioridad "high" | POST "/api/assignments/reassign/" con {"ticket_id": "TK-300", "priority": "high"} | 200 OK AND priority="high" AND NO se publica evento | ⏳ Pendiente | |
| US-04-SC-03 | US-04 — Reasignar prioridad | Ticket sin asignación previa | no existe asignación para TK-999 | POST "/api/assignments/reassign/" con {"ticket_id": "TK-999", "priority": "medium"} | 400 Bad Request AND mensaje "no existe asignación" | ⏳ Pendiente | |
| US-04-SC-04 | US-04 — Reasignar prioridad | Prioridad inválida | asignación para TK-300 | POST "/api/assignments/reassign/" con {"ticket_id": "TK-300", "priority": "urgent"} | 400 Bad Request AND prioridades válidas | ⏳ Pendiente | |
| US-05-SC-01 | US-05 — Asignar/reasignar usuario | Asignación exitosa | asignación ID 5 sin usuario | PATCH "/api/assignments/5/assign-user/" con {"assigned_to": "agent-15"} | 200 OK AND assigned_to="agent-15" | ⏳ Pendiente | |
| US-05-SC-02 | US-05 — Asignar/reasignar usuario | Reasignación de usuario | asignación ID 5 con "agent-10" | PATCH "/api/assignments/5/assign-user/" con {"assigned_to": "agent-20"} | 200 OK AND assigned_to="agent-20" | ⏳ Pendiente | |
| US-05-SC-03 | US-05 — Asignar/reasignar usuario | Desasignación | asignación ID 5 con "agent-10" | PATCH "/api/assignments/5/assign-user/" con {"assigned_to": null} | 200 OK AND assigned_to=null | ⏳ Pendiente | |
| US-05-SC-04 | US-05 — Asignar/reasignar usuario | Asignación inexistente | no existe ID 999 | PATCH "/api/assignments/999/assign-user/" con {"assigned_to": "agent-15"} | 400 Bad Request AND "no existe la asignación" | ⏳ Pendiente | |
| US-06-SC-01 | US-06 — Eliminar asignación | Eliminación exitosa | asignación ID 7 | DELETE "/api/assignments/7/" | 204 No Content AND asignación no existe en BD | ⏳ Pendiente | |
| US-06-SC-02 | US-06 — Eliminar asignación | Eliminar inexistente | no existe ID 888 | DELETE "/api/assignments/888/" | 404 Not Found | ⏳ Pendiente | |
| US-06-SC-03 | US-06 — Eliminar asignación | Verificación post-eliminación | asignación ID 7 fue eliminada | GET "/api/assignments/7/" | 404 Not Found | ⏳ Pendiente | |

### EP-02: Procesamiento de Eventos

| ID | US | Escenario | Given | When | Then | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
| US-07-SC-01 | US-07 — Creación automática por evento ticket.created | Asignación creada por evento | consumer conectado AND no existe asignación TK-500 | mensaje event_type="ticket.created", ticket_id="TK-500", priority="medium" | asignación TK-500 creada con prioridad "medium" AND evento assignment.created publicado | ⏳ Pendiente | |
| US-07-SC-02 | US-07 — Creación automática por evento ticket.created | Evento duplicado (idempotencia) | asignación TK-500 ya existe | mensaje ticket.created TK-500 de nuevo | no se crea nueva asignación AND existente sin cambios | ⏳ Pendiente | |
| US-07-SC-03 | US-07 — Creación automática por evento ticket.created | Mensaje malformado → DLQ | mensaje con JSON inválido o campos faltantes | handler intenta procesar | basic_nack sin requeue AND mensaje enrutado a DLQ | ⏳ Pendiente | |
| US-08-SC-01 | US-08 — Actualización prioridad por evento | Prioridad actualizada | asignación TK-600 con prioridad "low" | evento ticket.priority_changed, ticket_id="TK-600", new_priority="high" | prioridad actualizada a "high" | ⏳ Pendiente | |
| US-08-SC-02 | US-08 — Actualización prioridad por evento | Ticket sin asignación | no existe asignación TK-700 | evento ticket.priority_changed TK-700, new_priority="medium" | procesado sin error AND no se crea asignación | ⏳ Pendiente | |
| US-08-SC-03 | US-08 — Actualización prioridad por evento | Prioridad inválida rechazada | asignación TK-600 | evento ticket.priority_changed, new_priority="critical" | error de validación AND prioridad no cambia | ⏳ Pendiente | |

### EP-03: Contenerización

| ID | US | Escenario | Given | When | Then | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
| US-09-SC-01 | US-09 — Contenerización Docker | Construcción imagen | Dockerfile válido en raíz | docker build -t assignment-service . | imagen construida sin errores AND contiene deps de requirements.txt | ⏳ Pendiente | |
| US-09-SC-02 | US-09 — Contenerización Docker | Ecosistema docker-compose | Dockerfile y docker-compose.yml | docker-compose up -d | servicios API, PostgreSQL y RabbitMQ activos AND API responde AND BD acepta conexiones | ⏳ Pendiente | |
| US-09-SC-03 | US-09 — Contenerización Docker | Persistencia tras reinicio | ecosistema corriendo AND asignaciones creadas | docker-compose down + docker-compose up -d | asignaciones previas disponibles AND datos persisten | ⏳ Pendiente | |

### EP-04: Calidad Continua

| ID | US | Escenario | Given | When | Then | Resultado | Observaciones |
|---|---|---|---|---|---|---|---|
| US-10-SC-01 | US-10 — Pipeline CI GitHub Actions | Pipeline automático | .github/workflows/ci.yml existe | push a rama feature/nueva-funcionalidad | pipeline se dispara AND construye entorno AND ejecuta tests | ⏳ Pendiente | |
| US-10-SC-02 | US-10 — Pipeline CI GitHub Actions | Pipeline bloquea si test falla | PR hacia develop | un test unitario falla | status "failed" en rojo AND PR bloqueado AND detalle del fallo visible | ⏳ Pendiente | |
| US-10-SC-03 | US-10 — Pipeline CI GitHub Actions | Pipeline reporta cobertura | pipeline exitoso | todos los tests pasan | cobertura ≥ 70% AND status "success" en verde | ⏳ Pendiente | |

## Firma / Sign-off

| Campo | Valor |
|---|---|
| Nombre del tester | ______________________________ |
| Fecha de ejecución | ______________________________ |
| Rol / Equipo | ______________________________ |
| Resultado global (✅/❌/⏳) | ______________________________ |
| Comentarios finales | ______________________________ |
