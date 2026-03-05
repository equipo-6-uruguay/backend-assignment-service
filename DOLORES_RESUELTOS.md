# DOLORES_RESUELTOS.md — Registro de Dolores/Bugs Resueltos

**Proyecto:** Assignment Service (Django + DDD + EDA)  
**Fecha de creación:** 26 de Febrero, 2026  
**Propósito:** Mantener separados los dolores activos (`DOLORES.md`) de los ya resueltos para evitar confusiones.

---

## 1. Criterio de movimiento

Un dolor/bug se mueve desde `DOLORES.md` a este archivo **solo cuando**:

1. Existe evidencia en `develop` de que el cambio ya está aplicado, y
2. Está respaldado por historial de trabajo (Issue/PR cerrada o commit verificable), y
3. No rompe el comportamiento esperado de tests/contrato.

---

## 2. Revisión actual (2026-03-05)

### Resultado del repositorio GitHub

- Issues cerradas vinculadas a dolores: **4** (#1, #3, #13, #15)
- Pull Requests de remediacion mergeadas vinculadas: **7** (#2, #4, #12, #14, #16, #17, #18)
- Pull Requests abiertas relacionadas con remediacion: **0**

### Resultado en código (`develop`)

Se migraron **13 dolores** por cierre y merge de quick wins/correcciones en `develop`:

- `CFG-01` — credenciales RabbitMQ hardcodeadas
- `SEC-01` — falta de fail-fast con `ALLOWED_HOSTS` vacío en producción
- `SEC-02` — fallback de CSRF no condicionado por entorno
- `NOM-01` — typo en docstring ("autoridad" → "prioridad")
- `NOM-02` — import muerto (`random`)
- `TST-02` — inconsistencia de rutas API en tests vs router real
- `SCL-01` — sin paginación global en API
- `DOC-01` — serializer sin validaciones explícitas del contrato de entrada
- `EDA-01` — ACK prematuro del mensaje antes de confirmar procesamiento real
- `EDA-02` — tarea Celery sin retry/backoff/autoretry explícitos
- `ERR-02` — `except Exception` genérico en publisher y adapter
- `CPL-01` — ViewSet desacoplado de infraestructura concreta mediante Composition Root
- `CPL-02` — Handler desacoplado de infraestructura concreta por evento mediante container compartido

---

## 3. Registro de dolores migrados

| ID | Estado | Fecha migración | Evidencia |
|---|---|---|---|
| CFG-01 | ✅ Resuelto | 2026-02-26 | Issue #1 cerrado + PR #2 mergeado |
| SEC-01 | ✅ Resuelto | 2026-02-26 | Issue #1 cerrado + PR #2 mergeado |
| SEC-02 | ✅ Resuelto | 2026-02-26 | Issue #1 cerrado + PR #2 mergeado |
| NOM-01 | ✅ Resuelto | 2026-02-26 | Issue #1 cerrado + PR #2 mergeado |
| NOM-02 | ✅ Resuelto | 2026-02-26 | Issue #1 cerrado + PR #2 mergeado |
| TST-02 | ✅ Resuelto | 2026-02-27 | Issue #3 cerrado + PR #4 mergeado |
| SCL-01 | ✅ Resuelto | 2026-02-27 | PR #14 mergeado |
| DOC-01 | ✅ Resuelto | 2026-02-27 | PR #14 mergeado |
| EDA-01 | ✅ Resuelto | 2026-02-27 | PR #16 mergeado |
| EDA-02 | ✅ Resuelto | 2026-02-27 | PR #16 mergeado |
| ERR-02 | ✅ Resuelto | 2026-02-27 | PR #16 mergeado |
| CPL-01 | ✅ Resuelto | 2026-02-27 | PR #12 mergeado |
| CPL-02 | ✅ Resuelto | 2026-02-27 | PR #12 mergeado |

---

## 4. Historial de movimientos

| Fecha | IDs movidos | Evidencia | Responsable |
|---|---|---|---|
| 2026-02-26 | CFG-01, SEC-01, SEC-02, NOM-01, NOM-02 | Issue #1 cerrado / PR #2 mergeado en `develop` | Auditoría repo |
| 2026-02-27 | TST-02 | Issue #3 cerrado / PR #4 mergeado en `main` | Auditoría repo |
| 2026-02-27 | SCL-01, DOC-01 | PR #14 mergeado en `develop` | Auditoría repo |
| 2026-02-27 | EDA-01, EDA-02, ERR-02 | PR #16 mergeado en `develop` | Auditoría repo |
| 2026-02-27 | CPL-01, CPL-02 | PR #12 mergeado en `develop` | Auditoría repo |