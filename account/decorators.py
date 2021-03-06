from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserAccountAuthenticationForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect


def unthentication_user(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:  # checking of user
            return view_func(request, *args, **kwargs)
        else:
            return wrap(request, *args, **kwargs)
    return wrap


def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_admin == 1:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_user(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 0:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_staff(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 1:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
