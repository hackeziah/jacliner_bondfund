import json
import uuid
import datetime
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.models import Company, Position,UserAccount,UserInfo
from bond_fund.models import TransactionType,Requests,Account,TransacType
from account.decorators import user_is_staff, user_is_user, user_is_admin
from account.forms import CompanyForm, PositionForm
from bond_fund.forms import TransactionManageForm,RequestForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core import serializers

def load_transaction(request,id):
    # ttype = TransacType.objects.only('id').get(id=id)
    data_item = TransactionType.objects.filter(ttype=id)
    return render(request,'requests/add-request.html',{'data_item':data_item});
    #     data = serializers.serialize('json',TransactionType.objects.filter(ttype=ttype))
    #     return JsonResponse(data,safe=False)
    # else:
    #     return JsonResponse({'data': 'failure'})

def all_request_view(request):
    title = "All Request"
    contentheader = "Manage All Request"
    data = Requests.objects.filter(trash=0)
    template = "requests/all-request.html"
    data_transac = TransactionType.objects.filter(trash=0)   # data_ac =
# .order_by('-date_created')
    content = {
        'title' : title,
        'contentheader' : contentheader,
        'data': data,
        'data_transac' : data_transac
    }

    return render(request,template,content)

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def view_request(request):
    if request.method == "GET":
        request_no = request.GET.get('request_no', None)
        data_request = Requests.objects.get(request_no= str(request_no))
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
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def change_request_status(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        data = Requests.objects.get(id=int(id))
        data.status = request.GET.get('status', None)
        data.save()
    return HttpResponseRedirect('/all-request')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def request_trash(request):
    if request.GET:
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
    user_info = UserInfo.objects.get(id=int(2))
    fullname = user_info.last_name + ", " + user_info.first_name
    data_transac_save = TransactionType.objects.filter(trash=0,ttype=1)
    data_transac_deduc = TransactionType.objects.filter(trash=0, ttype=2)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            data = Requests(
                request_no=codeGenerator(),
                account_no = request.POST['account_no'],
                status=0,
                amount = form.cleaned_data['amount'],
                remark = request.POST['remark'],
                trash=0,
                clerk= fullname,
                transaction_id = request.POST['transaction_id'],
            );
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

# def transaction_view(request):
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


# def add_request_form(request):
#     if request.method == 'POST':
#         form = RequestForm(request.POST)
#         if form.is_valid():
#             data = Requests(
#                 account_no = form.cleaned_data['account_no'],
#                 transaction_id = request.POST['transaction_id'],
#                 amount = form.cleaned_data['amount'],
#                 remark = request.POST['remark'],
#                 status=0,
#                 trash=0,
#                 request_no=codeGenerator(),
#             );
#             data.save()
#             messages.success(request, 'Request was Created!')
#             return HttpResponseRedirect('/add-request')

#     else:
#         form = RequestForm()
#     return render(request, 'requests/add-request.html', {'request_form': form})