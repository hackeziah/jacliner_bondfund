from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.models import Company, Position
from bond_fund.models import TransactionType,Requests
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

    content = {
        'title' : title,
        'contentheader' : contentheader,
        'data': data
    }
    return render(request,template,content)