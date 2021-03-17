import datetime
import json
import uuid

from django.views.generic import TemplateView
# from chartjs.views.lines import BaseLineChartView
from bond_fund.models import *
from account.models import *

from django.shortcuts import render
from django.http.response import JsonResponse
from itertools import count
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from account.decorators import user_is_staff, user_is_user

from bond_fund.filters import TransactionFilter, DeductionTransactionFilter, SavingsTransactionFilter

from account.forms import CompanyForm, PositionForm
from django.contrib import messages
from account.models import Company, Position, UserAccount, UserInfo
from bond_fund.forms import RequestForm, TransactionManageForm

from bond_fund.models import Account, Requests, TransactionType, TransacType
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


###########CREATE TRANSACTION####################################

@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def create_transaction_staff(request, request_no):
    title = 'Create Transaction'
    main = "Transaction"
    contentheader = 'Create Transaction'
    template = "staff/transactions/create-transaction.html"
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
            return HttpResponseRedirect('/all-request-view-staff')
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


def codeGeneratorTransac():
    now = datetime.datetime.now()
    year = now.year
    ramdom = uuid.uuid4().hex[:6].upper()
    finalramdom = str('TRANS-') + str(year)+'-'+str(ramdom)
    return finalramdom


def done_transaction_staff(request):

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
    return HttpResponseRedirect('/all-transaction-staff')

##########CREATE TRANSACTION####################

##########REQUEST TRANSACTION####################


def all_request_view_staff(request):
    title = "All Request"
    contentheader = "Manage All Request"
    data = Requests.objects.filter(trash=0)
    template = "staff/requests/all-request.html"
    data_transac = TransactionType.objects.filter(
        trash=0).order_by('date_created')
    headerform = "Manage Request"
    content = {
        'title': title,
        'contentheader': contentheader,
        'headerform': headerform,
        'data': data,
        'data_transac': data_transac
    }

    return render(request, template, content)


def all_pending_view_staff(request):
    title = "Pending Request"
    contentheader = "Pending Request"
    data = Requests.objects.filter(trash=0, status=0).order_by('date_created')
    template = "staff/requests/all-pending-request.html"
    headerform = "Manage Request"
    content = {
        'title': title,
        'contentheader': contentheader,
        'headerform': headerform,
        'data': data
    }
    return render(request, template, content)


def all_approve_view_staff(request):
    title = "Approve Request"
    contentheader = "Approve Request"
    data = Requests.objects.filter(trash=0, status=1).order_by('date_created')
    template = "staff/requests/all-approve-request.html"
    headerform = "Manage Request"
    content = {
        'title': title,
        'contentheader': contentheader,
        'headerform': headerform,
        'data': data
    }
    return render(request, template, content)


def all_disapprove_view_staff(request):
    title = "Disapprove Request"
    contentheader = "Disapprove Request"
    data = Requests.objects.filter(trash=0, status=2).order_by('date_created')
    template = "staff/requests/all-disapprove-request.html"
    headerform = "Manage Request"
    content = {
        'title': title,
        'contentheader': contentheader,
        'headerform': headerform,
        'data': data
    }
    return render(request, template, content)

# view-status-request -filter


def view_status_request(request):
    status = request.GET.get('status', None)
    data = Requests.objects.filter(status=int(status))
    data = list(data.values())
    return JsonResponse(data, safe=False)


def view_request(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        if request.is_ajax():
            data_request = Requests.objects.get(id=str(id))
            account_no = data_request.account_no
            data_account = Account.objects.get(account_no=str(account_no))
            data_accountinfo = UserInfo.objects.get(emp_no=data_account.empno)
            data_transac = TransactionType.objects.filter(trash=0)
            fullname = data_accountinfo.last_name+", "+data_accountinfo.first_name
            transac_type = data_request.transaction.ttype.name
            transac_detail = data_request.transaction.name
            date = str(data_request.date_created)
            data = {
                'request_no': data_request.request_no,
                'amount': data_request.amount,
                'account_no': data_request.account_no,
                'status': data_request.status,
                'remark': data_request.remark,
                'realease_by': data_request.clerk,
                'date_created': date,
                'transac_type': transac_type,
                'transac_detail': transac_detail,
                'balance': data_account.balance,
                'employee_no': data_accountinfo.emp_no,
                'fullname': fullname,
                'company': data_accountinfo.company_name.company_name,
                'position': data_accountinfo.position_name.position_name,
            }

    return JsonResponse(data)

##########REQUEST TRANSACTION####################

# All Transactions


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def all_transaction_staff(request):
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
    return render(request, 'staff/transactions/all-transaction.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def deduction_transaction_staff(request):
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
    return render(request, 'staff/transactions/deduction-transactions.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def saving_transaction_staff(request):
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
    return render(request, 'staff/transactions/saving-transaction.html', content)


def view_transaction_staff(request):
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
@user_is_staff
def transaction_item_view(request):
    title = 'All Transaction'
    contentheader = 'Manage All Transaction'

    content = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'staff/transactions/all-transaction.html', content)


# All Transactions


# Add Request

def load_transaction(request, id):
    data_item = TransactionType.objects.filter(ttype=id)
    return render(request, 'staff/requests/add-request.html', {'data_item': data_item})


def codeGenerator():
    now = datetime.datetime.now()
    year = now.year
    ramdom = uuid.uuid4().hex[:6].upper()
    finalramdom = str('REQ-') + str(year)+'-'+str(ramdom)
    return finalramdom


@login_required(login_url=reverse_lazy('account:login'))
def add_request_staff(request):
    title = "Add Request"
    contentheader = "Creating Request"
    user = request.session['user']
    user_info = UserInfo.objects.get(user_id=user)
    # acc = Account.objects.get(empno_id=userinfo.id)
    fullname = user_info.last_name + ", " + user_info.first_name
    data_transac_save = TransactionType.objects.filter(trash=0, ttype=1)
    data_transac_deduc = TransactionType.objects.filter(trash=0, ttype=2)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            account_no = request.POST['account_no']
            account = Account.objects.get(account_no=str(account_no))
            balance = account.balance
            amount = form.cleaned_data['amount']
            transaction_id = request.POST['transaction_id']
            trans = TransactionType.objects.get(id=transaction_id)
            ttype = trans.ttype_id

            data = Requests(
                request_no=codeGenerator(),
                account_no=request.POST['account_no'],
                status=0,
                amount=amount,
                remark=request.POST['remark'],
                trash=0,
                clerk=fullname,
                transaction_id=request.POST['transaction_id'],
                transactionttype=trans.ttype.name,
                transactiontname=trans.name
            )
            if (int(ttype) == 2):
                if float(amount) >= float(balance):
                    messages.warning(
                        request, 'Insuficent balance in this ACCOUNT! ' + account_no)
                else:
                    data.save()
                    messages.success(request, 'Request was Created!')
                    return HttpResponseRedirect('/add-request-staff')
            else:

                data.save()
                messages.success(request, 'Request was Created!')
                return HttpResponseRedirect('/add-request-staff')
    else:
        form = RequestForm()
    content = {
        'title': title,
        'contentheader': contentheader,
        'savings': data_transac_save,
        'deduction': data_transac_deduc,
        # 'data_trac':data_trac,
        'request_form': form
    }
    return render(request, 'staff/requests/add-request.html', content)
# Add Request

# staff transaction
@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def all_transaction_view_staff(request):
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
    return render(request, 'staff/transactions/all-transaction.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def deduction_transaction_view_staff(request):
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
    return render(request, 'staff/transactions/deduction-transactions.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def saving_transaction_view_staff(request):
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
    return render(request, 'staff/transactions/saving-transaction.html', content)

# staff transaction


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def staff_dashboard_view(request):
    title = "Staff Dashboard"
    contentheader = "Staff Dashboard"
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
    return render(request, 'staff/dashboard.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def request_data_staff(request):
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
@user_is_staff
def request_data_status_staff(request):
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
@user_is_staff
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
