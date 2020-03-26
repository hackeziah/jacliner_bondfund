from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.decorators import user_is_staff, user_is_user, user_is_admin


@login_required(login_url=reverse_lazy('account:login'))
@user_is_user
def user_dashboard_view(request):
    title = "User-Dashboard"
    contentheader = 'Dashboard'
    context = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'user/dashboard.html', context)
