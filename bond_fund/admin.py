from django.contrib import admin

# Register your models here.

from .models import Transaction, TransactionType, Account, Request, TransactionItem, TransactionType


admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(Account)
admin.site.register(Request)
admin.site.register(TransactionItem)
# admin.site.register(TransactionType)
