import uuid
from datetime import timedelta
from decimal import Decimal

from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def auth_client(client):
    # Аутентификация с jwt
    user = User.objects.create_user(username='testuser', password='testpass')
    token = AccessToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client

@pytest.fixture
def test_organization():
    from core.models import Organization
    return Organization.objects.create(
        inn="1234567890",
        balance=Decimal("100000.00")
    )


@pytest.fixture
def test_payment(test_organization):
    from core.models import Payment
    return Payment.objects.create(
        operation_id=uuid.uuid4(),
        organization=test_organization,
        amount=Decimal("5000.00"),
        document_number="TEST-001",
        document_date=timezone.now() - timedelta(days=1)
    )


@pytest.fixture
def valid_webhook_data():
    return {
        "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4b",
        "amount": 10000.00,
        "payer_inn": "1234567890",
        "document_number": "PAY-2023-001",
        "document_date": "2024-04-27T21:00:00Z"
    }
