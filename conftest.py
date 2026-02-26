"""
Root conftest.py for pytest-django configuration.

Sets the required environment variables before Django settings are loaded,
so tests can run without a .env file (CI-friendly).
"""
import os

# Provide sensible defaults for CI / local pytest runs
os.environ.setdefault("ASSIGNMENT_SERVICE_SECRET_KEY", "test-secret-key-not-for-prod")
os.environ.setdefault("DJANGO_DEBUG", "true")
os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "*")
os.environ.setdefault("POSTGRES_DB", "assignment_db")
os.environ.setdefault("POSTGRES_USER", "assignment_user")
os.environ.setdefault("POSTGRES_PASSWORD", "assignment_pass")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
