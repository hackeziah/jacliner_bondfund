from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.models import Company, Position
from bond_fund.models import TransactionType,Requests,Account
from account.decorators import user_is_staff, user_is_user, user_is_admin
from account.forms import CompanyForm, PositionForm
from bond_fund.forms import TransactionManageForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def all_request_view(request):
    title = "All Request"
    contentheader = "Manage All Request"

    data = Requests.objects.filter(trash=0)
    template = "requests/all-request.html"
    data_transac = TransactionType.objects.filter(trash=0)
    # data_ac =

    content = {
        'title' : title,
        'contentheader' : contentheader,
        'data': data,
        'data_transac' : data_transac

    }

    return render(request,template,content)

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

def add_request(request):
    title = "Add Request"
    contentheader = "Creating Request"
    data_transac_save = TransactionType.objects.filter(trash=0,ttype="Savings")
    data_transac_deduc = TransactionType.objects.filter(trash=0, ttype="Deduction")
    content = {
        'title' : title,
        'contentheader' :contentheader,
        'savings': data_transac_save,
        'deduction': data_transac_deduc
    }

            # <!-- `id`, `request_no`, `account_no`, `status`, `amount`, `remark`, `clerk`,
            #                             `trash`, `date_created`, `date_modified`, `transaction_id` -->
    template = "requests/add-request.html"
    return render(request,template,content);