from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from bond_fund.models import UserAccount, TransactionType, Account, Transaction
from account.models import UserInfo
from django.shortcuts import get_object_or_404


class TransactionManageForm(forms.Form):
    ttype = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ' '}))
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ' '}))


class TransactionForm(forms.Form):
    status = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ' '}))


class RequestForm(forms.Form):
    account_no = forms.CharField(required=True)
    amount = forms.CharField(required=True)

    def clean_account_no(self):
        try:
            Account.objects.get(
                account_no__iexact=self.cleaned_data['account_no'], trash=0)
        except Account.DoesNotExist:
            raise forms.ValidationError(("The account does not exist"))


class UserAddForm(forms.Form):
    emp_no = forms.CharField(required=True)
    balance = forms.IntegerField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(required=True)

    def clean_emp_no(self):
        if UserInfo.objects.filter(emp_no=self.cleaned_data['emp_no']).exists():
            raise forms.ValidationError(("The Employee number had been use"))

    def clean_email(self):
        if UserAccount.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(("The email had been use"))

        #     def clean(self):
        # if self.is_valid():
        #     email = self.cleaned_data['email']
        #     password = self.cleaned_data['password']
        #     if not authenticate(email=email, password=password):
        #         raise forms.ValidationError("Invalid login")
