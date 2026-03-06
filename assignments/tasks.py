"""
Celery tasks con política de reintentos para resiliencia ante fallos transitorios.
"""
import logging

from celery import shared_task
from django.db import OperationalError, InterfaceError
import pika.exceptions
from typing import Dict, Any

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(
        OperationalError,
        InterfaceError,
        pika.exceptions.AMQPConnectionError,
        pika.exceptions.StreamLostError,
        pika.exceptions.ConnectionClosedByBroker,
        pika.exceptions.ChannelClosedByBroker,
    ),
    retry_backoff=2,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=5,
)
def process_ticket_event(self, event_data: Dict[str, Any]) -> None:
    """
    Celery task que procesa eventos de ticket en segundo plano.

    Política de reintentos:
        - Reintenta automáticamente ante errores transitorios de DB o broker
          (OperationalError, InterfaceError, AMQPConnectionError, etc.).
        - Backoff exponencial: factor 2, máximo 60s, con jitter.
        - Máximo 5 reintentos antes de marcar la tarea como fallida.
        - Errores de validación (ValueError, TypeError) NO se reintentan.

    Args:
        self: Instancia de la tarea (bind=True).
        event_data: Diccionario con los datos del evento.
    """
    logger.info(
        "Processing ticket event (attempt %d/%d): %s",
        self.request.retries + 1,
        self.max_retries + 1,
        event_data.get('event_type', 'unknown'),
    )
    from messaging.handlers import handle_ticket_event
    handle_ticket_event(event_data)
