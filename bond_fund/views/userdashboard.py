from django.views.generic import TemplateView
from bond_fund.models import *
from account.models import *

from django.shortcuts import render
from django.http.response import JsonResponse
from itertools import count
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from account.decorators import user_is_user, user_is_user

from bond_fund.filters import TransactionFilter, DeductionTransactionFilter, SavingsTransactionFilter

# user transaction
@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def all_transaction_view_user(request):
    title = 'All Transaction'
    contentheader = 'Manage All Transaction'
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    account_no = acc.account_no
    account_id = acc.id

    data = Transaction.objects.filter(
        trash=0, account_id=account_id).order_by('-date_created')
    myFilter = TransactionFilter(request.GET, queryset=data)
    data = myFilter.qs
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'myFilter': myFilter
    }

    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'myFilter': myFilter
    }
    return render(request, 'user/transaction/all-transaction.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def deduction_transaction_view_user(request):
    title = 'All Deduction'
    contentheader = 'Manage All Deduction'
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    account_no = acc.account_no
    account_id = acc.id

    data = Transaction.objects.filter(
        trash=0, ttype=2, account_id=account_id).order_by('date_created')
    myFilter = DeductionTransactionFilter(request.GET, queryset=data)
    data = myFilter.qs
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'myFilter': myFilter
    }
    return render(request, 'user/transaction/deduction-transactions.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def saving_transaction_view_user(request):
    title = "Savings"
    contentheader = 'Manage Savings'
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    account_no = acc.account_no
    account_id = acc.id
    data = Transaction.objects.filter(
        trash=0, ttype=1, account_id=account_id).order_by('date_created')
    myFilter = SavingsTransactionFilter(request.GET, queryset=data)
    data = myFilter.qs
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'myFilter': myFilter
    }
    return render(request, 'user/transaction/saving-transaction.html', content)

# user transaction


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def user_dashboard_view(request):
    title = "user Dashboard"
    contentheader = "user Dashboard"
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)

    account_no = acc.account_no
    account_id = acc.id

    trans = Transaction.objects.filter(trash=0, account_id=account_id).count()
    req = Requests.objects.filter(trash=0, account_no=account_no).count()
    acc = Account.objects.filter(trash=0).count()
    account = Account.objects.get(trash=0, account_no=account_no)
    balance = account.balance

    account_dec = Transaction.objects.filter(
        trash=0, account_id=account_id, ttype_id=2)
    account_save = Transaction.objects.filter(
        trash=0, account_id=account_id, ttype_id=1)

    a = []
    for item in account_dec:
        a.append(item.amount)
    total_deduction = sum(a)

    b = []
    for item in account_save:
        b.append(item.amount)
    total_save = sum(b)

    content = {
        'title': "Dashboard",
        'contentheader': "Dashboard Charts",
        'total_trans': trans,
        'total_req': req,
        'total_deduction': f"{total_deduction:,}",
        'total_save':  f"{total_save:,}",
        'total_money': f"{balance:,}"
    }
    return render(request, 'user/dashboard.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def request_data_user(request):
    labels = []
    data = []
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    account_no = acc.account_no
    account_id = acc.id

    transaction_list_s = Transaction.objects.filter(
        trash=0, ttype=1, account_id=account_id).count()
    transaction_list_d = Transaction.objects.filter(
        trash=0, ttype=2, account_id=account_id).count()

    labels.append(["Savings"])
    labels.append(["Deduction"])
    data.append([transaction_list_s])
    data.append([transaction_list_d])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def request_data_status_user(request):
    labels = []
    data = []
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    account_no = acc.account_no
    r_list_pending = Requests.objects.filter(
        status=0, account_no=account_no).count()
    t_list_app = Requests.objects.filter(
        status=1, account_no=account_no).count()
    t_list_disapp = Requests.objects.filter(
        status=2, account_no=account_no).count()
    t_list_done = Requests.objects.filter(
        status=4, account_no=account_no).count()

    labels.append("Pending")
    labels.append("Apptrove")
    labels.append("Dispprove")
    labels.append("Done")

    data.append([r_list_pending])
    data.append([t_list_disapp])
    data.append([t_list_app])
    data.append([t_list_done])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def count_users(requests):
    labels = []
    data = []

    user = UserInfo.objects.filter(trash=0).count()
    user = UserInfo.objects.filter(trash=0).count()

    labels.append("Pending")
    labels.append("Apptrove")
    labels.append("Dispprove")
    labels.append("Done")

    data = {
        'labels': labels,
        'data': data,
    }
    return JsonResponse(data)
