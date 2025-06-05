# payments/serializers.py
from rest_framework import serializers
from django.utils import timezone


class BankWebhookSerializer(serializers.Serializer):
    operation_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    payer_inn = serializers.CharField(max_length=12)
    document_number = serializers.CharField(max_length=100)
    document_date = serializers.DateTimeField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной")
        return value

    def validate_document_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError("Дата документа не может быть в будущем")
        return value


class BalanceSerializer(serializers.Serializer):
    inn = serializers.CharField(max_length=12)
    balance = serializers.DecimalField(max_digits=15, decimal_places=2)
