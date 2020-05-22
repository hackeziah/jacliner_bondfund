import datetime
import json
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from account.decorators import user_is_admin, user_is_staff, user_is_user
from account.forms import CompanyForm, PositionForm
from account.models import Company, Position, UserAccount, UserInfo
from bond_fund.forms import RequestForm, TransactionManageForm
from bond_fund.models import Account, Requests, TransactionType, TransacType

from bond_fund.serializers import RequestsSerializer
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    UpdateAPIView
)

def load_transaction(request,id):
    data_item = TransactionType.objects.filter(ttype=id)
    return render(request,'requests/add-request.html',{'data_item':data_item});

def all_request_view(request):
    title = "All Request"
    contentheader = "Manage All Request"
    data = Requests.objects.filter(trash=0)
    template = "requests/all-request.html"
    data_transac = TransactionType.objects.filter(trash=0).order_by('date_created')
    headerform = "Manage Request"
    content = {
        'title' : title,
        'contentheader' : contentheader,
         'headerform' :headerform,
        'data': data,
        'data_transac' : data_transac
    }

    return render(request,template,content)

def all_pending_view(request):
    title = "Pending Request"
    contentheader = "Pending Request"
    data = Requests.objects.filter(trash=0,status=0).order_by('date_created')
    template = "requests/all-pending-request.html"
    headerform = "Manage Request"
    content = {
        'title' : title,
        'contentheader' : contentheader,
        'headerform' :headerform,
        'data': data
    }
    return render(request,template,content)

def all_approve_view(request):
    title = "Approve Request"
    contentheader = "Approve Request"
    data = Requests.objects.filter(trash=0,status=1).order_by('date_created')
    template = "requests/all-approve-request.html"
    headerform = "Manage Request"
    content = {
        'title' : title,
        'contentheader' : contentheader,
        'headerform' :headerform,
        'data': data
    }
    return render(request,template,content)

def all_disapprove_view(request):
    title = "Disapprove Request"
    contentheader = "Disapprove Request"
    data = Requests.objects.filter(trash=0,status=2).order_by('date_created')
    template = "requests/all-disapprove-request.html"
    headerform = "Manage Request"
    content = {
        'title' : title,
        'contentheader' : contentheader,
        'headerform' :headerform,
        'data': data
    }
    return render(request,template,content)

# view-status-request -filter
def view_status_request(request):
    status = request.GET.get('status', None)
    data = Requests.objects.filter(status = int(status))
    data = list(data.values())
    return JsonResponse(data, safe=False)

def view_request(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        if request.is_ajax():
            data_request = Requests.objects.get(id= str(id))
            account_no = data_request.account_no
            data_account = Account.objects.get(account_no = str(account_no))
            data_accountinfo = UserInfo.objects.get(emp_no = data_account.empno)
            data_transac = TransactionType.objects.filter(trash=0)
            fullname=data_accountinfo.last_name+", "+data_accountinfo.first_name
            transac_type = data_request.transaction.ttype.name
            transac_detail = data_request.transaction.name
            date = str(data_request.date_created)
            data = {
                    'request_no' :data_request.request_no,
                    'amount' :data_request.amount,
                    'account_no' :data_request.account_no,
                    'status' :data_request.status,
                    'remark' : data_request.remark,
                    'realease_by' : data_request.clerk,
                    'date_created' : date,
                    'transac_type' :transac_type,
                    'transac_detail' :transac_detail,
                    'balance' : data_account.balance,
                    'employee_no': data_accountinfo.emp_no,
                    'fullname' : fullname,
                    'company' : data_accountinfo.company_name.company_name,
                    'position' : data_accountinfo.position_name.position_name,
                }

    return JsonResponse(data)

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def change_request_status(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        data = Requests.objects.get(id=int(id))
        # status =
        data.status = request.GET.get('status', None)
        data.save()
    return HttpResponseRedirect('/all-request')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def request_approve_checked(request):
    if request.GET:
        id = request.GET['id']
        data = Requests.objects.get(id=int(id))
        data.status = 1
        data.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def request_disapprove_checked(request):
    if request.GET:
        id = request.GET['id']
        data = Requests.objects.get(id=int(id))
        data.status = 2
        data.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def request_trash(request):
    if request.method == "GET":
        id = request.GET['trash_id']
        data = Requests.objects.get(id=int(id))
        data.trash = 1
        data.save()
    return HttpResponseRedirect('/all-request')

def codeGenerator():
    now = datetime.datetime.now()
    year = now.year
    ramdom = uuid.uuid4().hex[:6].upper()
    finalramdom = str('REQ-') + str(year)+'-'+str(ramdom)
    return finalramdom

def add_request(request):
    title = "Add Request"
    contentheader = "Creating Request"
    user = request.session['user']
    user_info = UserInfo.objects.get(id=int(user))
    fullname = user_info.last_name + ", " + user_info.first_name
    data_transac_save = TransactionType.objects.filter(trash=0,ttype=1)
    data_transac_deduc = TransactionType.objects.filter(trash=0, ttype=2)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            account_no = request.POST['account_no']
            account = Account.objects.get(account_no = str(account_no))
            balance = account.balance
            amount = form.cleaned_data['amount']
            transaction_id = request.POST['transaction_id']
            trans = TransactionType.objects.get(id = transaction_id)
            ttype = trans.ttype_id

            data = Requests(
                request_no=codeGenerator(),
                account_no = request.POST['account_no'],
                status=0,
                amount = amount,
                remark = request.POST['remark'],
                trash=0,
                clerk= fullname,
                transaction_id = request.POST['transaction_id'],
                transactionttype = trans.ttype.name,
                transactiontname =trans.name
                );
            if (int(ttype) == 2):
                if float(amount) >= float(balance):
                    messages.warning(request, 'Insuficent balance in this ACCOUNT! ' + account_no )
                else:
                    data.save()
                    messages.success(request, 'Request was Created!')
                    return HttpResponseRedirect('/add-request')
            else:

                data.save()
                messages.success(request, 'Request was Created!')
                return HttpResponseRedirect('/add-request')
    else:
        form = RequestForm()
    content = {
        'title' : title,
        'contentheader' :contentheader,
        'savings': data_transac_save,
        'deduction': data_transac_deduc,
        # 'data_trac':data_trac,
        'request_form':form
    }
    return render(request,'requests/add-request.html',content);

def transaction_view(request):
    data = TransactionType.objects.filter(trash=0)
    contentheader = "Manage Transaction"
    title = "Maintenance Transaction"

    if request.method == 'POST':
        form = TransactionManageForm(request.POST)
        if form.is_valid():
            data = TransactionType(
                ttype=form.cleaned_data['ttype'],
                name=request.POST['name'],
                trash=0,
            )
            data.save()
            messages.success(request, 'Transaction was Created!')
            return HttpResponseRedirect('/transaction-setup')
    else:
        form = TransactionManageForm()
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'transaction_form': form

    }
    template = 'settings/transaction.html'

    return render(request, template, content)
