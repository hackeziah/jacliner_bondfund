from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('account:login'))
def deduction_view(request):
    contentheader = "Manage Deduction"
    title = "Maintenance Deduction"
    content = {
        'title': title,
        'contentheader': contentheader
    }
    return render(request, 'settings/deduction.html', content)


@login_required(login_url=reverse_lazy('account:login'))
def company_view(request):
    contentheader = "Manage Company"
    title = "Maintenance Company"
    content = {
        'title': title,
        'contentheader': contentheader
    }
    return render(request, 'settings/company.html', content)


@login_required(login_url=reverse_lazy('account:login'))
def position_view(request):
    contentheader = "Manage Position"
    title = "Maintenance Position"
    content = {
        'title': title,
        'contentheader': contentheader
    }
    return render(request, 'settings/position.html', content)
