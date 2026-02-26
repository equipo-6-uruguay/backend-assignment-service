# Cada repo debe tener un workflow que:

- Se ejecute en push/PR a main, develop, feature/**
- Instale dependencias
- Corra tests
- Falla si los tests fallan

---

# Publicación de imágenes (Paso siguiente)

Actualmente nadie publicó imágenes.

Debemos hacer que cada repo:

1. Construya su imagen Docker.
2. La publique en GitHub Container Registry (GHCR).

Ejemplo futuro:

ghcr.io/equipo-6-uruguay/backend-ticket-service:latest

Sin esto, el repo infra no puede orquestar nada.

---

# Qué hace el repo INFRA

El repo infra no tiene código de negocio.

**Debe contener**:

- docker-compose.yml
- .env.example
- README.md

**El docker-compose debe**:

- Usar imágenes ya publicadas.
- No usar build.context a rutas locales.
- Definir redes y dependencias.
- Levantar todo el sistema.

**Ejemplo conceptual**:

ticket-service:
  image: ghcr.io/equipo-6-uruguay/backend-ticket-service:latest

---

# Flujo correcto de trabajo

1. Dev hace cambios en su repo.
2. CI corre tests.
3. Se construye la imagen.
4. Se publica en GHCR.
5. Infra usa esa imagen.
6. docker compose up levanta el stack completo.

---

# Responsabilidades claras

Backend:
- Dockerfile correcto.
- Tests funcionando.
- Imagen publicable.

Frontend:
- Build reproducible.
- Dockerfile optimizado (multi-stage recomendado).
- Variables de entorno claras.

Infra:
- Orquestación.
- No builda código.
- No contiene lógica.

---

# Punto crítico actual

Antes de avanzar con infra, necesitamos:

- Agregar workflow de publicación de imágenes en cada repo.
- Definir convención de tags (latest / develop / v1.0.0).

Sin imágenes publicadas, la arquitectura distribuida no está completa.

---

# Resultado esperado

Sistema desacoplado.
Servicios independientes.
Build reproducible.
Deploy orquestado.
Arquitectura profesional.