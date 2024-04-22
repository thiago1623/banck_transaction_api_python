"""serializers for transaction management api"""
from rest_framework import serializers

from ..models import Transaction

# pylint: disable=too-few-public-methods


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the endpont that get all transaction"""
    class Meta:
        """Meta class."""
        model = Transaction
        fields = '__all__'
