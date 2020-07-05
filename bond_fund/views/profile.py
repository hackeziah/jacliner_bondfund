
import json
import uuid
import datetime
from decimal import *
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from account.decorators import user_is_staff, user_is_user, user_is_admin

from django.contrib import messages
from django.core.exceptions import ValidationError
# mymodels
from account.models import Company, Position, UserAccount, UserInfo
from bond_fund.models import TransactionType, Requests, Account, TransacType, Transaction
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash


@login_required(login_url=reverse_lazy('account:login'))
# @user_is_admin
def profile_view(request):
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    useraccinfo = UserAccount.objects.get(id=user)
    accountinfo = UserInfo.objects.get(user_id=user)

    content = {
        'title': "Profile",
        'contentheader': "Profile Information",
        'userinfo': userinfo,
        'accountinfo': accountinfo,
        'useraccinfo': useraccinfo,


    }
    return render(request, 'staff/profile/index.html', content)


def change_profile_info(request):
    if request.method == "GET":
        user = request.session['user']
        userinfo = UserInfo.objects.get(user_id=user)
        acc = Account.objects.get(empno_id=userinfo.id)
        useraccinfo = UserAccount.objects.get(id=user)
        accountinfo = UserInfo.objects.get(user_id=user)

        userinfo.last_name = request.GET.get('last_name', None)
        userinfo.first_name = request.GET.get('first_name', None)
        userinfo.mobile_number = request.GET.get('mobile_number', None)

        useraccinfo.email = request.GET.get('email', None)
        useraccinfo.set_password(request.GET.get('password', None))
        userinfo.save()
        useraccinfo.save()

    return HttpResponseRedirect('/profile')


@login_required(login_url=reverse_lazy('account:login'))
# @user_is_admin
def profile_view_my(request):
    user = request.session['user']
    userinfo = UserInfo.objects.get(user_id=user)
    acc = Account.objects.get(empno_id=userinfo.id)
    useraccinfo = UserAccount.objects.get(id=user)
    accountinfo = UserInfo.objects.get(user_id=user)

    content = {
        'title': "Profile",
        'contentheader': "Profile Information",
        'userinfo': userinfo,
        'accountinfo': accountinfo,
        'useraccinfo': useraccinfo,


    }
    return render(request, 'profile/index.html', content)


def change_profile_info_my(request):
    if request.method == "GET":
        user = request.session['user']
        userinfo = UserInfo.objects.get(user_id=user)
        acc = Account.objects.get(empno_id=userinfo.id)
        useraccinfo = UserAccount.objects.get(id=user)
        accountinfo = UserInfo.objects.get(user_id=user)

        userinfo.last_name = request.GET.get('last_name', None)
        userinfo.first_name = request.GET.get('first_name', None)
        userinfo.mobile_number = request.GET.get('mobile_number', None)

        useraccinfo.email = request.GET.get('email', None)
        useraccinfo.set_password(request.GET.get('password', None))
        userinfo.save()
        useraccinfo.save()

    return HttpResponseRedirect('/my-profile')

# @login_required(login_url=reverse_lazy('account:login'))
