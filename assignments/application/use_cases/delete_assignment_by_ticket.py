"""
Caso de uso para eliminar una asignación por el ID de ticket.
"""
from assignments.domain.repository import AssignmentRepository


class DeleteAssignmentByTicketIdUseCase:
    """
    Elimina una asignación buscando por el ticket_id.
    Este caso de uso es típicamente llamado por eventos de dominio (ej. ticket.deleted).
    No emite evento de assignment.deleted para evitar ciclos infinitos.
    """
    
    def __init__(self, repository: AssignmentRepository):
        self.repository = repository
        
    def execute(self, ticket_id: str) -> bool:
        """
        Ejecuta la eliminación.
        
        Args:
            ticket_id: ID del ticket cuya asignación se eliminará
            
        Returns:
            True si se eliminó, False si no existía.
        """
        assignment = self.repository.find_by_ticket_id(ticket_id)
        if not assignment:
            return False
            
        if assignment.id is not None:
            return self.repository.delete(assignment.id)
            
        return False
