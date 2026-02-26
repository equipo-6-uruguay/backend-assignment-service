# =============================================================================
# Dockerfile — Backend Assignment Service (optimizado)
# =============================================================================
FROM python:3.12-slim AS base

# Evita buffers en stdout/stderr y no genera .pyc
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# --- Dependencias (capa cacheada) ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Código fuente ---
COPY . .

# Recoger archivos estáticos (no falla si no hay STATIC_ROOT configurado)
RUN python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8001

# Comando por defecto: migrar + gunicorn (prod-ready)
# En docker-compose se puede sobreescribir con `command:`
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn assessment_service.wsgi:application --bind 0.0.0.0:8001 --workers 3 --timeout 120"]
