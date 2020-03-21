from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('account:login'))
def usermanagement_view(request):
    title = 'User Management'
    contentheader = 'Manage All Users'
    context = {
        'title': title,
        'contentheader': contentheader
    }
    return render(request, 'usermanagement/index.html', context)
