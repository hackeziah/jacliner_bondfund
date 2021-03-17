

from django.views.generic import TemplateView
# from chartjs.views.lines import BaseLineChartView
from bond_fund.models import *
from django.shortcuts import render
from django.http.response import JsonResponse
from itertools import count
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from account.decorators import user_is_admin, user_is_staff, user_is_user

@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def dashboard_charts(request):
    trans = Transaction.objects.filter(trash = 0).count()
    req  = Requests.objects.filter(trash=0).count()
    acc  = Account.objects.filter(trash=0).count()
    balance = Account.objects.filter(trash=0)
    a = []
    for item in balance:
        a.append(item.balance)
    total = sum(a)

    content = {
        'title': "Dashboard",
        'contentheader': "Dashboard Charts",
        'total_trans' : trans,
        'total_req' : req,
        'total_account' : acc,
        'total_money' : f"{total:,}"
            }
    return render(request, 'dashboard/index.html',content)

@login_required(login_url=reverse_lazy('account:login'))
def request_data(request):
    labels = []
    data = []

    transaction_list_s = Transaction.objects.filter(trash = 0,ttype = 1).count()
    transaction_list_d = Transaction.objects.filter(trash=0,ttype = 2).count()

    labels.append(["Savings"])
    labels.append(["Deduction"])
    data.append([transaction_list_s])
    data.append([transaction_list_d])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@login_required(login_url=reverse_lazy('account:login'))
def request_data_status(request):
    labels = []
    data = []
    r_list_pending = Requests.objects.filter(status = 0).count()
    t_list_app= Requests.objects.filter(status = 1).count()
    t_list_disapp = Requests.objects.filter(status = 2).count()
    t_list_done = Requests.objects.filter(status = 4).count()

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


def count_users(requests):
    labels = []
    data = []

    user = UserInfo.objects.filter(trash = 0).count()
    user = UserInfo.objects.filter(trash = 0).count()

    labels.append("Pending")
    labels.append("Apptrove")
    labels.append("Dispprove")
    labels.append("Done")

    data={
        'labels': labels,
        'data': data,
    }
    return JsonResponse(data)
