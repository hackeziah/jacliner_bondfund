
from django.db import models
from account.models import UserAccount, UserInfo
from django.utils import timezone

now = timezone.now()


class Account(models.Model):
    Pending = 0
    Approve = 1
    Disapprove = 2
    status_ch = (
        (Pending, "Pending"),
        (Approve, "Activate"),
        (Disapprove, "Deactivate"),
    )
    account_no = models.CharField(
        verbose_name="Acoount No", max_length=200, default="", unique=True)
    empno = models.ForeignKey(UserInfo,  on_delete=models.CASCADE)
    balance = models.DecimalField(
        verbose_name="Balance", default=None, max_digits=20, decimal_places=2)
    status = models.IntegerField(
        verbose_name="Status", default=0, choices=status_ch)

    trash = models.BooleanField(verbose_name="Trash", default=0)

    def __str__(self):
        return self.account_no

    def get_emp_name(self):
        return self.empno.first_name + " " + self.empno.last_name

    def get_emp_no(self):
        return self.empno.emp_no

    def get_emp_status(self):
        return self.empno.status

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
    name = models.CharField(max_length=20)
    ttype = models.ForeignKey(TransacType, on_delete=models.CASCADE)
    trash = models.BooleanField(verbose_name="Trash", default=False)

    def __str__(self):
        return self.name

    def get_type(self):
        return self.ttype.name

    def get_name(self):
        return self.ttype.name


class Requests(models.Model):
    request_no = models.CharField(verbose_name="Request No",
                                  max_length=254, blank=True, unique=True)
    account_no = models.CharField(max_length=254, verbose_name="Account No")
    status = models.IntegerField(
        verbose_name="status")
    amount = models.DecimalField(
        verbose_name="Amount", default=None, max_digits=20, decimal_places=2)
    remark = models.TextField(verbose_name="Remarks", default="")
    clerk = models.CharField(
        verbose_name="Bond Clerk", max_length=254)
    transaction = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE)
    transactionttype = models.CharField(
        verbose_name="Transaction Type", max_length=254)
    transactiontname = models.CharField(
        verbose_name="Transaction Name", max_length=254)
    # transactionname
    trash = models.BooleanField(verbose_name="Trash", default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_no

    def __str__(self):
        return self.transaction.ttype.name

    def get_transaction(self):
        return self.transaction.ttype.name

    def get_name(self):
        return self.transaction.name


class Transaction(models.Model):
    Pending = 1
    Approve = 2
    Disapprove = 3
    Done = 4
    status_ch = (
        (Pending, "Pending"),
        (Disapprove, "Disapprove"),
        (Approve, "Approve"),
        (Done, "Done")
    )

    transaction_no = models.CharField(verbose_name="Transaction No",
                                      max_length=254, blank=True, unique=True)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, default=None, related_name='transaction_account')
    request = models.ForeignKey(
        Requests, on_delete=models.CASCADE, default=None, related_name='transaction_request')
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(
        verbose_name="Amount", default=None, max_digits=20, decimal_places=2)
    last_balance = models.DecimalField(
        verbose_name="Last Balance",  max_length=254, max_digits=20, decimal_places=2)
    current_balance = models.DecimalField(
        verbose_name="Current Balance",  max_length=254, max_digits=20, decimal_places=2)
    remark = models.TextField(verbose_name="Remarks")
    realease_by = models.CharField(
        verbose_name="Release By", max_length=50, default="")
    status = models.IntegerField(
        verbose_name="Status", default=0, choices=status_ch)
    transactionttype = models.CharField(
        verbose_name="Transaction Type", max_length=254)
    ttype = models.ForeignKey(
        TransacType, on_delete=models.CASCADE)
    trash = models.BooleanField(verbose_name="Trash", default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_no

    def get_account_no(self):
        return self.account.account_no

    def get_fullname(self):
        return self.account.empno.first_name + " " + self.account.empno.last_name
