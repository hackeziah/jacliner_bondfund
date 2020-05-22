import uuid
import datetime
# from django.contrib.auth.models import UserAccount
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserAccountAuthenticationForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .decorators import unthentication_user

from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .decorators import user_is_staff, user_is_user, user_is_admin
from .models import UserAccount, UserInfo
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def logout_view(request):
    try:
      del request.session['user']
    except:
      pass
    logout(request)
    return redirect('account:login')


# @login_required(login_url=reverse_lazy('account:login'))

def login_view(request):
    context = {}
    user = request.user # paalam kung ano kung sino ung user na to
    if request.POST:
        form = UserAccountAuthenticationForm(request.POST)
        if form.is_valid:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                request.session['user'] = user.id
                if user.status == 1:
                    if user.is_admin == 1:
                        return redirect('account:admin-dashboard')
                    if user.is_user == 1:
                            return redirect('account:user-dashboard')
                    if user.is_staff == 1:
                            return redirect('account:staff-dashboard')
                else:
                    return render(request, 'accounts/login.html', {'error_message': 'Your account has been disabled please just with the approval of account'})
    else:
        form = UserAccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "accounts/login.html", context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Successfully Registered')
            return render(request, 'accounts/login.html', context)

        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/registration.html', context)


def codeGenerator():
    now = datetime.datetime.now()
    year = now.year
    ramdom = uuid.uuid4().hex[:6].upper()
    finalramdom = str(year)+'-'+str(ramdom)
    return finalramdom




@login_required(login_url=reverse_lazy('account:login'))
@user_is_admin
def admin_dashboard_view(request):
    title = "Dashboard"
    contentheader = 'Dashboard'
    context = {
        'title': title,
        'contentheader': contentheader

    }
    return render(request, 'transaction/dashboard.html', context)


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
