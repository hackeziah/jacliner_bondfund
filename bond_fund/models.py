
from django.db import models
from account.models import UserAccount, UserInfo


class Account(models.Model):
    account_no = models.CharField(
        verbose_name="Acoount No", max_length=200, default="", unique=True)
    empno = models.OneToOneField(UserInfo,  on_delete=models.CASCADE)
    balance = models.FloatField(verbose_name="Balance",  max_length=255)
    status = models.IntegerField(
        verbose_name="Status", default=0)
    trash = models.BooleanField(verbose_name="Trash", default=0)

    def __str__(self):
        return self.account_no

    def get_emp_name(self):
        return self.empno.first_name + " " + self.empno.last_name

    def get_emp_company(self):
        return self.empno.company_name

    def get_emp_position(self):
        return self.empno.position_name

class TransacType(models.Model):
    name = models.CharField(max_length=20)
    trash = models.BooleanField(verbose_name="Trash", default=False)

    def __str__(self):
        return self.name
class TransactionType(models.Model):
    ttype = models.ForeignKey(TransacType, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    trash = models.BooleanField(verbose_name="Trash", default=False)
    def __str__(self):
        return self.ttype

    def __str__(self):
        return self.ttype.name

    def get_name(self):
        return  self.ttype.name

class Transaction(models.Model):
    transaction_no = models.CharField(verbose_name="Transaction No",
                                      max_length=255, blank=True, unique=True)
    account_no = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="Amount",  max_length=255)
    last_balance = models.FloatField(
        verbose_name="Last Balance",  max_length=255)
    current_balance = models.FloatField(
        verbose_name="Current Balance",  max_length=255)
    remark = models.TextField(verbose_name="Remarks")
    clerk = models.CharField(
        verbose_name="Bond Clerk", max_length=50)
    status = models.IntegerField(
        verbose_name="Status", default=0)
    trash = models.BooleanField(verbose_name="Trash", default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_no

class Requests(models.Model):
    request_no = models.CharField(verbose_name="Request No",
                                  max_length=255, blank=True, unique=True)
    account_no = models.CharField(max_length=255,verbose_name="Account No")
    status = models.IntegerField(
        verbose_name="status")
    amount = models.FloatField(verbose_name="Amount",  max_length=255)
    remark = models.TextField(verbose_name="Remarks", default="")
    clerk = models.CharField(
        verbose_name="Bond Clerk", max_length=255)
    transaction = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE)
    trash = models.BooleanField(verbose_name="Trash", default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.request_no

    def __str__(self):
        return self.transaction.ttype.name


    def get_transaction(self):
        return  self.transaction.ttype.name

    def get_name(self):
        return  self.transaction.name

