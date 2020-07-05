
import json
import uuid
import datetime
from decimal import *
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.decorators import user_is_staff, user_is_user, user_is_admin
from account.forms import CompanyForm, PositionForm
from bond_fund.forms import TransactionManageForm, RequestForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core import serializers

from bond_fund.filters import TransactionFilter, DeductionTransactionFilter, SavingsTransactionFilter
# mymodels
from account.models import Company, Position, UserAccount, UserInfo
from bond_fund.models import TransactionType, Requests, Account, TransacType, Transaction


@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def all_transaction_view(request):
    title = 'All Transaction'
    contentheader = 'Manage All Transaction'
    data = Transaction.objects.filter(trash=0).order_by('-date_created')
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
    return render(request, 'transaction/all-transaction.html', content)

# staff transaction
@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def all_transaction_view_staff(request):
    title = 'All Transaction'
    contentheader = 'Manage All Transaction'
    data = Transaction.objects.filter(trash=0).order_by('-date_created')
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
    return render(request, 'staff/transaction/all-transaction.html', content)


def codeGeneratorTransac():
    now = datetime.datetime.now()
    year = now.year
    ramdom = uuid.uuid4().hex[:6].upper()
    finalramdom = str('TRANS-') + str(year)+'-'+str(ramdom)
    return finalramdom


@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def create_transaction(request, request_no):
    title = 'Create Transaction'
    main = "Transaction"
    contentheader = 'Create Transaction'
    template = "transaction/create-transaction.html"
    if request.method == "GET":
        try:
            data_request = Requests.objects.get(
                request_no=str(request_no), trash=0, status=1)
            account_no = data_request.account_no
            data_account = Account.objects.get(
                account_no=str(account_no), trash=0)
            data_accountinfo = UserInfo.objects.get(emp_no=data_account.empno)
            fullname = data_accountinfo.last_name+", "+data_accountinfo.first_name
        except:
            return HttpResponseRedirect('/all-request')
    content = {
        'title': title,
        'contentheader': contentheader,
        'main': main,
        'data_request': data_request,
        'data_account': data_account,
        'data_accountinfo': data_accountinfo,
        'fullname': fullname
    }
    return render(request, template, content)


def done_transaction(request):

    if request.method == "POST":
        user = request.session['user']
        user_info = UserInfo.objects.get(user_id=user)
        realease_by = user_info.last_name + ", " + user_info.first_name

        remark = request.POST.get('remark')
        transaction_id = request.POST.get('transaction_id')
        account_id = request.POST.get('account_id')
        request_id = request.POST.get('request_id')
        req = Requests.objects.get(id=int(request_id))
        trans = TransactionType.objects.get(id=int(transaction_id))
        acc = Account.objects.get(id=int(account_id))
        ttype = trans.ttype_id
        new_balance = request.POST.get('new_balance')
        transaction = Transaction(
            transaction_no=codeGeneratorTransac(),
            amount=req.amount,
            last_balance=acc.balance,
            current_balance=new_balance,
            remark=remark,
            status=4,
            trash=0,
            realease_by=realease_by,
            transaction_type=trans,
            account=acc,
            request=req,
            transactionttype=trans.ttype.name,
            ttype=trans.ttype
        )

        req.status = 4
        req.save()
        acc.balance = new_balance
        acc.save()
        transaction.save()
    return HttpResponseRedirect('/all-transaction')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def deduction_transaction_view(request):
    title = 'All Deduction'
    contentheader = 'Manage All Deduction'
    data = Transaction.objects.filter(
        trash=0, ttype=2).order_by('date_created')
    myFilter = DeductionTransactionFilter(request.GET, queryset=data)
    data = myFilter.qs
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'myFilter': myFilter
    }
    return render(request, 'transaction/deduction-transactions.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def saving_transaction_view(request):
    title = "Savings"
    contentheader = 'Manage Savings'
    data = Transaction.objects.filter(
        trash=0, ttype=1).order_by('date_created')
    myFilter = SavingsTransactionFilter(request.GET, queryset=data)
    data = myFilter.qs
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'myFilter': myFilter
    }
    return render(request, 'transaction/saving-transaction.html', content)


def view_transaction(request):
    if request.method == "GET":
        transaction_id = request.GET.get('transaction_id', None)
        if request.is_ajax():
            data_transaction = Transaction.objects.get(
                id=int(transaction_id), trash=0)
            transac_type = data_transaction.transaction_type.ttype.name
            transac_detail = data_transaction.transaction_type.name
            account_no = data_transaction.account.account_no
            data_account = Account.objects.get(account_no=str(account_no))

            employee_name = data_transaction.account.empno.last_name + \
                ", " + data_transaction.account.empno.first_name
            employee_number = data_transaction.account.empno.emp_no
            company = data_transaction.account.empno.company_name.company_name
            position = data_transaction.account.empno.position_name.position_name
            mobile_number = data_transaction.account.empno.mobile_number
            # data_request = Requests.objects.get(id= str())
            data = {
                'transaction_no': data_transaction.transaction_no,
                'amount': data_transaction.amount,
                'last_balance': data_transaction.last_balance,
                'current_balance': data_transaction.current_balance,
                'balance': data_transaction.account.balance,
                'remark': data_transaction.remark,
                'status': data_transaction.status,
                'realease_by': data_transaction.realease_by,
                'date_created': data_transaction.date_created,
                'transac_type': transac_type,
                'transac_detail': transac_detail,
                'account_no': account_no,
                'employee_name': employee_name,
                'employee_number': employee_number,
                'company': company,
                'position': position,
                'request_no': data_transaction.request.request_no,
                'mobile_number': mobile_number

            }

    return JsonResponse(data)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def transaction_item_view(request):
    title = 'All Transaction'
    contentheader = 'Manage All Transaction'

    content = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'transaction/all-transaction.html', content)
