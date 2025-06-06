from django.db import transaction

from core.handlers import OrganizationHandler, PaymentHandler, BalanceLogHandler


class PaymentProcessor:
    """
    Класс реализует бизнес логику процесса оплаты
    """

    @staticmethod
    @transaction.atomic
    def payment(data: dict) -> dict:

        """
        Метод обрабатывает платеж

        :param data: dict
        :return:
        """

        organization = OrganizationHandler.get_organization_by_inn(data["payer_inn"])
        payment, payment_created = PaymentHandler.get_or_create_payment(data["operation_id"],
                                                                        organization=organization,
                                                                        amount=data["amount"],
                                                                        document_number=data["document_number"],
                                                                        document_date=data["document_date"])

        if payment_created:
            balance_before = organization.balance
            amount = payment.amount
            new_balance = OrganizationHandler.update_balance(organization, payment)

            BalanceLogHandler.create_balance_log(payment=payment,
                                                 organization=organization,
                                                 balance_before=balance_before,
                                                 amount=amount,
                                                 balance_after=new_balance
                                                 )
