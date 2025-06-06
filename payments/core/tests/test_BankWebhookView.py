import json
from decimal import Decimal

import pytest

from core.models import Organization, Payment, BalanceLog

pytestmark = pytest.mark.django_db


def test_bank_webhook_success(client, valid_webhook_data):
    Organization.objects.create(inn=valid_webhook_data["payer_inn"], balance=Decimal("0.00"))

    response = client.post(
        '/api/webhook/bank/',
        data=json.dumps(valid_webhook_data),
        content_type='application/json'
    )

    assert response.status_code == 200
    # Проверяем, что объекты созданы
    assert Payment.objects.count() == 1
    assert BalanceLog.objects.count() == 1
    org = Organization.objects.get(inn=valid_webhook_data["payer_inn"])
    # Проверяем, что баланс организации увеличился
    assert org.balance == Decimal(valid_webhook_data["amount"])


def test_bank_webhook_duplicate_payment(client, valid_webhook_data, test_organization):
    # Первый запрос
    client.post(
        '/api/webhook/bank/',
        data=json.dumps(valid_webhook_data),
        content_type='application/json'
    )

    # Второй запрос с тем же operation_id
    response = client.post(
        '/api/webhook/bank/',
        data=json.dumps(valid_webhook_data),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert Payment.objects.count() == 1  # Не создался дубликат


def test_bank_webhook_invalid_data(client):
    invalid_data = {
        "operation_id": "invalid-uuid",
        "amount": "-100.00",
        "payer_inn": "123",
        "document_number": "",
        "document_date": "invalid-date"
    }

    response = client.post(
        '/api/webhook/bank/',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )

    assert response.status_code == 400

    errors = response.json()["error"]
    assert "operation_id" in errors
    assert "amount" in errors
    assert "document_number" in errors
    assert "document_date" in errors


def test_bank_webhook_new_organization(client, valid_webhook_data):
    # Организации с таким ИНН нет в базе
    valid_webhook_data["payer_inn"] = "99999999999"
    response = client.post(
        '/api/webhook/bank/',
        data=json.dumps(valid_webhook_data),
        content_type='application/json'
    )

    assert response.status_code == 400
