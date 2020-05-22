import uuid
import json
import datetime
# import pandas as pd

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core import serializers

from jacliner_bondfund import settings

from bond_fund.forms import UserAddForm
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from bond_fund.filters import UserManagementFilter
from account.models import Company, Position,UserAccount,UserInfo
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from bond_fund.models import TransactionType,Requests,Account,TransacType,Transaction

from account.decorators import user_is_admin, user_is_staff, user_is_user
@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def usermanagement_view(request):
    title = 'User Management'
    contentheader = 'Manage All Users'

    data = Account.objects.filter(trash=0)
    position = Position.objects.filter(trash=0)
    company = Company.objects.filter(trash=0)
    myFilter = UserManagementFilter(request.GET, queryset=data)
    data = myFilter.qs
    context = {
        'title': title,
        'contentheader': contentheader,
        'data' : data,
        'myFilter':myFilter,
        'position' : position,
        'company' : company
    }

    return render(request, 'usermanagement/index.html', context)

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
# 'bond_fund:change-user-status
def change_user_status(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        data = Account.objects.get(id=int(id))
        data.status = request.GET.get('status', None)

        ui = data.empno_id
        dataui = UserInfo.objects.get(id=ui)
        dataui.status = request.GET.get('status', None)
        acc = dataui.user_id
        dataua = UserAccount.objects.get(id=acc)
        dataua.role = request.GET.get('role', None)

        dataua.status = request.GET.get('status', None)

        data.save()
        dataui.save()
        dataua.save()

    return HttpResponseRedirect('user-management')

@login_required(login_url=reverse_lazy('account:login'))
def usermanagement_trash(request):
    if request.method == "GET":
        trash = request.GET.get('trash', None)
        data = Account.objects.get(id=int(trash))
        data.trash = 1
        data.save()
    return HttpResponseRedirect('user-management')

@login_required(login_url=reverse_lazy('account:login'))
def usermanagement_detail(request):
    if request.method == "GET":
        vid = request.GET.get('vid', None)
        if request.is_ajax():
            data = Account.objects.get(id=int(vid))
            ui = data.empno_id
            dataui = UserInfo.objects.get(id=ui)
            name = dataui.first_name +" "+ dataui.last_name
            account = data.account_no
            account_id = data.id
            requests = Requests.objects.filter(account_no= str(account)).values('amount','request_no','transactionttype', 'transactiontname','date_created' ).order_by('-date_created')
            transactions = Transaction.objects.filter(account_id= int(account_id)).values('transaction_no', 'amount', 'last_balance', 'current_balance','transactionttype','date_created').order_by('-date_created')
            balance = str(data.balance)
            response_data = {}
            response_data['account_no'] = data.account_no
            response_data['balance'] = balance
            response_data['emp_no'] = dataui.emp_no
            response_data['name'] = name
            response_data['requests'] = list(requests)
            response_data['transactions'] = list(transactions)
        else:
            HttpResponseRedirect('user-management')
    else:
        HttpResponseRedirect('user-management')
    return JsonResponse(response_data)







def codeGeneratorAccount():
    now = datetime.datetime.now()
    year = now.year
    ramdom = uuid.uuid4().hex[:7].upper()
    finalramdom = str('ACT-NO-') + str(year)+'-'+str(ramdom)
    return finalramdom

def codeGeneratorPassword():
    ramdom1 = uuid.uuid4().hex[:4].lower()
    ramdom2 = uuid.uuid4().hex[:4].lower()
    finalramdom =  str(ramdom1) + str(ramdom2)
    return finalramdom


# @login_required(login_url=reverse_lazy('account:login'))
def add_user(request):
    if request.method == 'POST':
        genPassword = codeGeneratorPassword()
        codeAccount = codeGeneratorAccount()
        emp_no = request.POST.get('emp_no')
        try:
            UserInfo.objects.get(emp_no__iexact = emp_no,trash = 0)
            user = UserAccount.objects.create_user(
                        username = codeAccount,
                        password = genPassword,
                        is_staff = True,
                        is_active = False,
                        is_superuser = False,
                        email = request.POST.get("email")
                    )
            user.save()
            u = UserAccount.objects.latest('id')

            company = Company.objects.get(id=request.POST.get("company"))
            position = Position.objects.get(id=request.POST.get("position"))

            userinfo = UserInfo(
                    emp_no = request.POST.get("emp_no"),
                    first_name = request.POST.get("first_name"),
                    last_name = request.POST.get("last_name"),
                    mobile_number = request.POST.get("mobile_number"),
                    status = 1,
                    trash = 0,
                    company_name = company,
                    position_name = position,
                    user_id= u.id
                )
            userinfo.save()

            ua = UserInfo.objects.latest('id')

            account = Account(
                        account_no = codeAccount,
                        balance = request.POST.get("balance"),
                        status = 0,
                        trash = 0,
                        empno_id = ua.id
                    )
            account.save()

            subject = "Bondfund System Password Generate"
            message = "This is the password for this Account "+ codeAccount + " password is " + genPassword
            to = request.POST.get('email')
            if subject and message and to:
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [to])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
        except UserInfo.DoesNotExist:
            raise messages.error(request, 'Emploee Number has been use')


    messages.success(request, 'User was Created!')
    return HttpResponseRedirect('user-management')
