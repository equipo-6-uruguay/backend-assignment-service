from rest_framework import serializers
from .models import TicketAssignment
from .domain.entities import Assignment


class TicketAssignmentSerializer(serializers.ModelSerializer):
    def validate_ticket_id(self, value: str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError('ticket_id no puede estar vacío')
        return value.strip()

    def validate_priority(self, value: str) -> str:
        if value not in Assignment.VALID_PRIORITIES:
            raise serializers.ValidationError(
                f'priority debe ser uno de {Assignment.VALID_PRIORITIES}'
            )
        return value

    class Meta:
        model = TicketAssignment
        fields = ['id', 'ticket_id', 'priority', 'assigned_at', 'assigned_to']
        read_only_fields = ['id', 'assigned_at']
