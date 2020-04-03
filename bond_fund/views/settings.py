from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.models import Company, Position
from bond_fund.models import TransactionType,TransacType
from account.decorators import user_is_staff, user_is_user, user_is_admin
from account.forms import CompanyForm, PositionForm
from bond_fund.forms import TransactionManageForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse


@login_required(login_url=reverse_lazy('account:login'))
def transaction_view(request):
    data_trac = TransacType.objects.filter(trash=0)
    data = TransactionType.objects.filter(trash=0)
    contentheader = "Manage Transaction"
    title = "Maintenance Transaction"

    if request.method == 'POST':
        form = TransactionManageForm(request.POST)
        if form.is_valid():
            trans = form.cleaned_data['ttype']
            ttype = TransacType.objects.only('id').get(id=trans)
            data = TransactionType(
                ttype=ttype,
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
        'data_trac' : data_trac,
        'transaction_form': form

    }

    return render(request, 'settings/transaction.html', content)
# Delete Company
@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def delete_transactionmanage(request):
    if request.GET:
        id = request.GET['id']
        data = TransactionType.objects.get(id=int(id))
        data.trash = 1
        data.save()
    return HttpResponseRedirect('/transaction-setup')

# edit-company-Show
@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def edit_transactionmanage(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        ttype = request.GET.get('ttype', None)
        ts = TransacType.objects.get(id=int(ttype))
        data = TransactionType.objects.get(id=int(id))
        data.ttype = ts
        data.name = request.GET.get('name', None)
        data.save()
    return HttpResponseRedirect('/transaction-setup')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def add_transactype(request):
    if request.method == "POST":
        data = TransacType(
            name=request.POST['name'],
            trash = 0
        )
        data.save()

    return HttpResponseRedirect('/transaction-setup')

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def delete_ttype(request,id):
    data = TransacType.objects.get(id=int(id))
    data.trash = 1
    data.save()
    return HttpResponseRedirect('/transaction-setup')

# All Company
@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def company_view(request):
    contentheader = "Manage Company"
    title = "Maintenance Company"
    data = Company.objects.filter(trash=0)

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            datas = Company(
                company_name=form.cleaned_data['company_name'],
                description=request.POST['description'],
                trash=0,
            )
            datas.save()
            messages.success(request, 'Company was Created!')
            return HttpResponseRedirect('/company-setup')
    else:
        form = CompanyForm()
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'company_form': form

    }

    return render(request, 'settings/company.html', content)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            data = Company(
                company_name=form.cleaned_data['company_name'],
                description=form.cleaned_data['description'],
                trash=0,
            )
            data.save()
            messages.success(request, 'Company was Created!')
            return HttpResponseRedirect('/company-setup')
    else:
        form = CompanyForm()
    return render(request, 'settings/company.html', {'company_form': form})

# Delete Company
@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin

def delete_company(request):
    if request.GET:
        id = request.GET['id']
        company = Company.objects.get(id=int(id))
        company.trash = 1
        company.save()
    return HttpResponseRedirect('/company-setup')
# edit-company-Show
@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def edit_company(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        company = Company.objects.get(id=int(id))
        company.company_name = request.GET.get('company_name', None)
        company.description = request.GET.get('description', None)
        company.save()
    return HttpResponseRedirect('/company-setup')

# this is for postion CRED


@login_required(login_url=reverse_lazy('account:login'))
def position_view(request):
    contentheader = "Manage Position"
    title = "Maintenance Position"
    data = Position.objects.filter(trash=0)

    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            datas = Position(
                position_name=form.cleaned_data['position_name'],
                description=request.POST['description'],
                trash=0,
            )
            datas.save()
            messages.success(request, 'Position was Created!')
            return HttpResponseRedirect('/position-setup')
    else:
        form = PositionForm()
    content = {
        'title': title,
        'contentheader': contentheader,
        'data': data,
        'position_form': form

    }
    return render(request, 'settings/position.html', content)
# add position


@login_required(login_url=reverse_lazy('account:login'))
def add_position(request):
    content = {}
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            data = Position(
                postion_name=form.clean_data['postion_name'],
                description=request.POST['description'],
                trash=0

            )
            data.save()
            messages.success(request, 'Postion was created')

    else:
        form = CompanyForm()
        content = {
            'position_form': form

        }
    return render(request, 'settings/position.html', content)


@login_required(login_url=reverse_lazy('account:login'))
def delete_postion(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        position = Position.objects.get(id=int(id))
        position.trash = 1
        position.save()
    return HttpResponseRedirect('/position-setup')

# edit position


def edit_postion(request):
    if request.method == "GET":
        id = request.GET.get('id', None)
        position = Position.objects.get(id=int(id))
        position.position_name = request.GET.get('position_name', None)
        position.description = request.GET.get('description', None)
        position.save()
    return HttpResponseRedirect('/position-setup')
