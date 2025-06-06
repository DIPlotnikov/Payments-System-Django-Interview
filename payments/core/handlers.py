from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import BalanceLog, Organization, Payment


class OrganizationHandler:
    """
    Класс-обработчик модели организации
    """

    @staticmethod
    def update_balance(organization: Organization,
                       payment: Payment,
                       ) -> Decimal:
        """
        Безопасное изменение баланса с транзакцией

        :param organization: Организация
        :param payment: Связанный платеж

        :return: Новый баланс

        :raises ValidationError: При недостатке средств
        :raises TypeError: При пустом аргументе payment
        """

        amount = payment.amount
        organization.balance += amount
        organization.save()

        return organization.balance

    @staticmethod
    def get_organization_by_inn(inn: str) -> Organization:
        """
        Получение организации по ИНН

        :param inn: ИНН
        :return: Организация
        """
        try:
            return Organization.objects.get(inn=inn)
        except Organization.DoesNotExist:
            raise ValidationError(f"Организация с ИНН {inn} не найдена")
        except Exception as e:
            raise e

    @staticmethod
    def get_organization_balance(inn: str) -> Decimal:
        """
        Получение баланса организации

        :param inn: ИНН
        :return: Баланс
        """
        try:
            return Organization.objects.get(inn=inn).balance
        except Organization.DoesNotExist:
            return None
        except Exception as e:
            raise e


class PaymentHandler:
    """
    Класс-обработчик модели платежа
    """

    @staticmethod
    def get_or_create_payment(operation_id: str,
                              organization: Organization,
                              amount: Decimal,
                              document_number: str,
                              document_date: str
                              ) -> Payment:
        """
        Получение или создание платежа

        :param organization:
        :param operation_id: Идентификатор платежа
        :return: кортеж (Payment, created(bool))
        """

        return Payment.objects.get_or_create(operation_id=operation_id,
                                             defaults={"organization": organization,
                                                       "amount": amount,
                                                       "document_number": document_number,
                                                       "document_date": document_date}
                                             )


class BalanceLogHandler:

    @staticmethod
    def create_balance_log(payment: Payment, organization: Organization, amount: Decimal, balance_before: Decimal,
                           balance_after: Decimal):
        return BalanceLog.objects.create(payment=payment, organization=organization,
                                         amount=amount,
                                         balance_before=balance_before,
                                         balance_after=balance_after
                                         )
