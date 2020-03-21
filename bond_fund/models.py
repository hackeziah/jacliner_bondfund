
from django.db import models


from account.models import UserAccount


class Account(models.Model):
    account_no = models.CharField(
        verbose_name="Acoount No", max_length=200, default="", unique=True)
    userno = models.CharField(
        verbose_name="User No", max_length=255)
    balance = models.FloatField(verbose_name="Balance",  max_length=255)
    status = models.CharField(
        verbose_name="Status", max_length=40, default="0")
    trash = models.CharField(
        verbose_name="Trash", max_length=40, default="0")

    def __str__(self):
        return self.account_no


class TransactionType(models.Model):
    transaction_name = models.CharField(
        verbose_name="Transaction Name", max_length=50)
    description = models.TextField(
        verbose_name="Description", max_length=255)

    def __str__(self):
        return self.transaction_name


class Transaction(models.Model):
    transaction_no = models.CharField(verbose_name="Transaction No",
                                      max_length=255, blank=True, unique=True)
    account_no = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE)
    last_balance = models.FloatField(
        verbose_name="Last Balance",  max_length=255)
    current_balance = models.FloatField(
        verbose_name="Current Balance",  max_length=255)
    amount = models.FloatField(verbose_name="Amount",  max_length=255)
    touch_by = models.CharField(
        verbose_name="Touch By", max_length=50, unique=True)
    status = models.CharField(
        verbose_name="Status", max_length=40, default="0")
    trash = models.CharField(
        verbose_name="Trash", max_length=40, default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
