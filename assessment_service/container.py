"""
Composition Root para dependencias de Assignment Service.

Centraliza la construcción de repositorio, publisher y casos de uso.
"""
from dataclasses import dataclass
from typing import Optional

from assignments.application.event_publisher import EventPublisher
from assignments.application.use_cases.change_assignment_priority import ChangeAssignmentPriority
from assignments.application.use_cases.create_assignment import CreateAssignment
from assignments.application.use_cases.reassign_ticket import ReassignTicket
from assignments.application.use_cases.update_assigned_user import UpdateAssignedUser
from assignments.application.use_cases.delete_assignment import DeleteAssignmentUseCase
from assignments.domain.repository import AssignmentRepository


@dataclass(frozen=True)
class AssignmentContainer:
    """Container con todas las dependencias de aplicación para assignments."""

    repository: AssignmentRepository
    event_publisher: EventPublisher
    create_assignment: CreateAssignment
    reassign_ticket: ReassignTicket
    update_assigned_user: UpdateAssignedUser
    change_assignment_priority: ChangeAssignmentPriority
    delete_assignment: DeleteAssignmentUseCase


_container: Optional[AssignmentContainer] = None


def get_assignment_container() -> AssignmentContainer:
    """Retorna singleton del container de assignments."""
    global _container
    if _container is None:
        from assignments.infrastructure.messaging.event_publisher import RabbitMQEventPublisher
        from assignments.infrastructure.repository import DjangoAssignmentRepository

        repository = DjangoAssignmentRepository()
        event_publisher = RabbitMQEventPublisher()
        _container = AssignmentContainer(
            repository=repository,
            event_publisher=event_publisher,
            create_assignment=CreateAssignment(repository, event_publisher),
            reassign_ticket=ReassignTicket(repository, event_publisher),
            update_assigned_user=UpdateAssignedUser(repository, event_publisher),
            change_assignment_priority=ChangeAssignmentPriority(repository, event_publisher),
            delete_assignment=DeleteAssignmentUseCase(repository, event_publisher),
        )
    return _container


def reset_container() -> None:
    """Resetea singleton del container. Utilizado por tests."""
    global _container
    _container = None
