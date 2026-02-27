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

## 2. Revisión actual (2026-02-27)

### Resultado del repositorio GitHub

- Issues cerradas vinculadas a dolores: **2** (#1, #3) + **1 abierta en implementación** (#13)
- Pull Requests mergeadas vinculadas: **2** (#2, #4)
- Pull Requests abiertas relacionadas con documentación/tests: **2** (#6, #8)

### Resultado en código (`develop`)

Se migraron **8 dolores** por cierre y merge de quick wins/correcciones (incluye 2 en implementación activa en rama feature):

- `CFG-01` — credenciales RabbitMQ hardcodeadas
- `SEC-01` — falta de fail-fast con `ALLOWED_HOSTS` vacío en producción
- `SEC-02` — fallback de CSRF no condicionado por entorno
- `NOM-01` — typo en docstring ("autoridad" → "prioridad")
- `NOM-02` — import muerto (`random`)
- `TST-02` — inconsistencia de rutas API en tests vs router real
- `SCL-01` — sin paginación global en API
- `DOC-01` — serializer sin validaciones explícitas del contrato de entrada

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
| SCL-01 | 🟡 Implementado (pendiente merge a `develop`) | 2026-02-27 | Issue #13 + rama `feature/paginación-global-y-validación-http` |
| DOC-01 | 🟡 Implementado (pendiente merge a `develop`) | 2026-02-27 | Issue #13 + rama `feature/paginación-global-y-validación-http` |

---

## 4. Historial de movimientos

| Fecha | IDs movidos | Evidencia | Responsable |
|---|---|---|---|
| 2026-02-26 | CFG-01, SEC-01, SEC-02, NOM-01, NOM-02 | Issue #1 cerrado / PR #2 mergeado en `develop` | Auditoría repo |
| 2026-02-27 | TST-02 | Issue #3 cerrado / PR #4 mergeado en `main` | Auditoría repo |
| 2026-02-27 | SCL-01, DOC-01 | Issue #13 abierto + implementación en rama `feature/paginación-global-y-validación-http` (pendiente PR/merge a `develop`) | Auditoría repo |
