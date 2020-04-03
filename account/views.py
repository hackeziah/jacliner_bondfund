import uuid
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserAccountAuthenticationForm, RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import UserAccount
from .decorators import unthentication_user

from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .decorators import user_is_staff, user_is_user, user_is_admin
from .models import UserAccount, UserInfo
from django.contrib import messages


def logout_view(request):
    try:
      del request.session['user']
    except:
      pass
    logout(request)
    return redirect('account:login')


# @login_required
def login_view(request):
    context = {}
    user = request.user  # paalam kung ano kung sino ung user na to
    if request.POST:
        form = UserAccountAuthenticationForm(request.POST)
        if form.is_valid:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                request.session['user'] = user.id
                if user.is_admin == 1:
                    return redirect('account:admin-dashboard')
                if user.is_user == 1:
                    return redirect('account:user-dashboard')
                if user.is_staff == 1:
                    return redirect('account:staff-dashboard')
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
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            useraccount = authenticate(email=email, password=raw_password)
            login(request, useraccount)
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
