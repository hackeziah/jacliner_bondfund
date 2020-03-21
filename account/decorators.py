from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserAccountAuthenticationForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect


def unthentication_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:  # checking of user
            return redirect('bond_fund:user-dashboard')
        else:
            return wrap(request, *args, **kwargs)
    return wrap


# def userpermission(function):
#     def wrap(request, *args, **kwargs):
#         user = request.user
#         if user.is_user == 1:
#             return redirect('bond_fund:user-dashboard')
#         if user.is_admin == 1:
#             return redirect('bond_fund:dashboard')
#         if user.is_staff == 1:
#             return redirect('bond_fund:staff-dashboard')
#     return wrap


def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_admin == 1:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_staff(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_staff == 1:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_user(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_user == 1:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
