from django.db import models


class Organization(models.Model):
    """
    Модель для хранения данных организации
    """
    inn = models.CharField(max_length=12, unique=True,  db_index=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Организация {self.inn}"

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Payment(models.Model):
    """
    Модель для хранения данных о платежах
    """
    operation_id = models.UUIDField(unique=True,  db_index=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    document_number = models.CharField(max_length=50,  db_index=True)
    document_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Оплата № {self.operation_id}"

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'


class BalanceLog(models.Model):
    """
    Модель для хранения логов баланса
    """
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(auto_now_add=True)

    balance_before = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Лог баланса организации {self.organization.inn}: {self.amount}"

    class Meta:
        verbose_name = 'Лог баланса'
        verbose_name_plural = 'Логи баланса'
