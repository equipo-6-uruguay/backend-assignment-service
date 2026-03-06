"""
Implementación del EventPublisher usando RabbitMQ.
"""
import json
import logging
import os

import pika
import pika.exceptions
from typing import Optional

from assignments.domain.events import DomainEvent
from assignments.application.event_publisher import EventPublisher

logger = logging.getLogger(__name__)


class RabbitMQEventPublisher(EventPublisher):
    """
    Implementación concreta del EventPublisher usando RabbitMQ.
    
    Publica eventos de dominio a un exchange de RabbitMQ.
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        exchange: Optional[str] = None
    ):
        self.host = host or os.environ.get('RABBITMQ_HOST', 'rabbitmq')
        self.exchange = exchange or os.environ.get(
            'RABBITMQ_EXCHANGE_ASSIGNMENT', 
            'assignment_events'
        )
    
    def publish(self, event: DomainEvent) -> None:
        """
        Publica un evento de dominio a RabbitMQ.
        
        Args:
            event: Evento a publicar

        Raises:
            pika.exceptions.AMQPConnectionError: Si no se puede conectar al broker.
            pika.exceptions.AMQPChannelError: Si hay error a nivel de canal.
        """
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            channel = connection.channel()
            
            channel.exchange_declare(
                exchange=self.exchange,
                exchange_type='fanout',
                durable=True
            )
            
            message = json.dumps(event.to_dict())
            
            channel.basic_publish(
                exchange=self.exchange,
                routing_key='',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent
                    content_type='application/json'
                )
            )
            
            connection.close()
            
            logger.info(
                "Evento publicado exitosamente: %s",
                event.to_dict().get('event_type', 'unknown'),
            )

        except pika.exceptions.AMQPConnectionError as exc:
            logger.error("Error de conexión al broker RabbitMQ: %s", exc)
            raise
        except pika.exceptions.AMQPChannelError as exc:
            logger.error("Error de canal RabbitMQ: %s", exc)
            raise
        except Exception as exc:
            logger.exception("Error inesperado publicando evento: %s", exc)
            raise
