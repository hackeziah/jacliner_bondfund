from django.contrib import admin

# Register your models here.

from .models import Transaction, TransactionType, Account, Requests, TransacType


admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(Account)
admin.site.register(Requests)
admin.site.register(TransacType)


