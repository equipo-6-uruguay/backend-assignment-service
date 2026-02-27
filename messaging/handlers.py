"""
Handlers refactorizados para usar el adaptador de eventos.
"""
from typing import Dict, Any
from assessment_service.container import get_assignment_container

from assignments.infrastructure.messaging.event_adapter import TicketEventAdapter


def handle_ticket_event(event_data: Dict[str, Any], container=None) -> None:
    """
    Procesa eventos de ticket usando el adaptador.
    
    Args:
        event_data: Diccionario con los datos del evento
    """
    container = container or get_assignment_container()
    adapter = TicketEventAdapter(container.repository, container.event_publisher)
    
    event_type = event_data.get('event_type', 'ticket.created')
    
    if event_type == 'ticket.created':
        adapter.handle_ticket_created(event_data)
    elif event_type == 'ticket.priority_changed':
        adapter.handle_ticket_priority_changed(event_data)
    else:
        print(f"[ASSIGNMENT] Tipo de evento no manejado: {event_type}")
