from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.decorators import user_is_staff, user_is_user, user_is_admin
# #for user-management


@login_required(login_url=reverse_lazy('account:login'))
def all_transaction_view(request):
    title = 'All Transaction'
    contentheader = 'Manage All Transaction'

    context = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'transaction/all-transaction.html', context)


@login_required(login_url=reverse_lazy('account:login'))
def deduction_transaction_view(request):
    title = 'All Deduction'
    contentheader = 'Manage All Deduction'

    context = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'transaction/deduction-transactions.html', context)


@login_required(login_url=reverse_lazy('account:login'))
def saving_transaction_view(request):
    title = "Savings"
    contentheader = 'Manage Savings'
    context = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'transaction/saving-transaction.html', context)
