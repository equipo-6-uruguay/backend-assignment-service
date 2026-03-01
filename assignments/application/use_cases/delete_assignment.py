"""
Caso de uso para eliminar una asignación.
"""
from datetime import datetime

from assignments.domain.repository import AssignmentRepository
from assignments.application.event_publisher import EventPublisher
from assignments.domain.events import AssignmentDeleted


class DeleteAssignmentUseCase:
    """
    Elimina una asignación y publica un evento de dominio.
    """
    
    def __init__(self, repository: AssignmentRepository, event_publisher: EventPublisher):
        self.repository = repository
        self.event_publisher = event_publisher
        
    def execute(self, assignment_id: int) -> bool:
        """
        Ejecuta la eliminación.
        
        Args:
            assignment_id: ID de la asignación a eliminar
            
        Returns:
            True si se eliminó, False si no existía.
        """
        assignment = self.repository.find_by_id(assignment_id)
        if not assignment:
            return False
            
        if self.repository.delete(assignment_id):
            # Emitir evento
            event = AssignmentDeleted(
                assignment_id=assignment.id,
                ticket_id=assignment.ticket_id,
                occurred_at=datetime.now()
            )
            self.event_publisher.publish(event)
            return True
            
        return False
