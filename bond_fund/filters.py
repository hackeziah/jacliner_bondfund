import django_filters
from django_filters import DateFilter, CharFilter,ModelChoiceFilter

from bond_fund.models import *
from account.models import *


class TransactionFilter(django_filters.FilterSet):
	class Meta:
		model = Transaction
		fields = ['ttype','transaction_type']


class DeductionTransactionFilter(django_filters.FilterSet):
	transaction_type = ModelChoiceFilter(queryset=TransactionType.objects.filter(ttype=2))
	class Meta:
		model = Transaction
		fields = ['transaction_type']



class SavingsTransactionFilter(django_filters.FilterSet):
	transaction_type = ModelChoiceFilter(queryset=TransactionType.objects.filter(ttype=1))
	class Meta:
		model = Transaction
		fields = ['transaction_type']

class UserManagementFilter(django_filters.FilterSet):
	class Meta:
		model = Account
		fields = ['status']
	# position = ModelChoiceFilter(queryset= Position.objects.all())
	# company = ModelChoiceFilter(queryset= Company.objects.all())
	# status_ch = (
    #     (0, "Pending"),
    #     (1, "Activate"),
    #     (2, "Deactivate"),
    # )
    # status_role = (
    #     (0, "Admin"),
    #     (1, "Staff"),
    #     (2, "User"),
    # )
	# status = ModelChoiceFilter(all = status_ch)
