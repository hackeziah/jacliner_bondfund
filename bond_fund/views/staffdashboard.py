from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.decorators import user_is_staff, user_is_user, user_is_admin


@login_required(login_url=reverse_lazy('account:login'))
@user_is_staff
def staff_dashboard_view(request):
    title = "Staff Dashboard"
    contentheader = 'Dashboard'
    context = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'staff/dashboard.html', context)
