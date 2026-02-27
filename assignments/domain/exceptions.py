"""
Excepciones de dominio para el módulo de assignments.
Jerarquía tipada que reemplaza ValueError genérico.
"""


class DomainException(Exception):
    """Base para todas las excepciones de dominio."""
    pass


class AssignmentNotFound(DomainException):
    """La asignación solicitada no existe."""
    pass


class InvalidPriority(DomainException):
    """La prioridad proporcionada no es válida."""
    pass


class InvalidTicketId(DomainException):
    """El ticket_id proporcionado es inválido o vacío."""
    pass
