from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.handlers import OrganizationHandler
from core.processors import PaymentProcessor
from core.serializers import BankWebhookSerializer, BalanceSerializer


class BankWebhookView(APIView):
    """
    Webhook для банка
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Webhook для банка
        """
        try:
            serializer = BankWebhookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'error': serializer.errors}, status=400)

            data = serializer.validated_data
            PaymentProcessor.payment(data)

            return Response(status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class OrganizationBalanceView(APIView):
    """
    Получение баланса организации
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, inn):
        try:
            balance = OrganizationHandler.get_organization_balance(inn)

            if balance is None:
                return Response(
                    {"error": "Организация не найдена"},
                    status=404
                )

            serializer = BalanceSerializer({
                'inn': inn,
                'balance': balance
            })
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
