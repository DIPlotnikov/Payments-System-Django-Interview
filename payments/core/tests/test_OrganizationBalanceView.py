import pytest

pytestmark = pytest.mark.django_db

def test_organization_balance_success(client, test_organization):
    response = client.get(f'/api/organizations/{test_organization.inn}/balance/')

    assert response.status_code == 200
    assert response.json() == {
        "inn": test_organization.inn,
        "balance": str(test_organization.balance)
    }


def test_organization_balance_not_found(client):
    response = client.get('/api/organizations/0000000000/balance/')

    assert response.status_code == 404
    assert response.json() == {"error": "Организация не найдена"}