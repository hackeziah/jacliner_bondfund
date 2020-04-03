from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from bond_fund.models import UserAccount,TransactionType,Account



class TransactionManageForm(forms.Form):
    ttype = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ' '}))
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': ' '}))

class RequestForm(forms.Form):
     account_no = forms.CharField(required=True)
     amount = forms.CharField(required=True)

     def clean_account_no(self):
         try:
            Account.objects.get(account_no__iexact = self.cleaned_data['account_no'])
         except Account.DoesNotExist:
            raise forms.ValidationError(("The account does not exist"))

    #  def clean_amount(self):
    #      mybal = Account.objects.values_list('balance').filter(account_no = 'ACT-3303003')
    #      if self.cleaned_data['amount'] > mybal:
    #          raise forms.ValidationError(("Working"))
    #      return self.cleaned_data



    #  def clean_amount(self):
    #      try:



# try:
#             User.objects.get(email=self.cleaned_data['email'])
#         except User.DoesNotExist:
#             return self.cleaned_data['email']
#         raise forms.ValidationError(_("The email already exists. Please try another one."))
        # def clean_email(self):
        #     try:
        #         User.objects.get(email__iexact=self.cleaned_data['email'])
        #     except User.DoesNotExist:
        #         return self.cleaned_data['email']
        #     raise forms.ValidationError(_("The email already exists. Please try another one."))

# class UserAccountAuthenticationForm(forms.ModelForm):
#     password = forms.CharField(label="Password", widget=forms.PasswordInput)

#     class Meta:
#         model = UserAccount
#         fields = ('email', 'password')

#     def clean(self):
#         if self.is_valid():
#             email = self.cleaned_data['email']
#             password = self.cleaned_data['password']
#             if not authenticate(email=email, password=password):
#                 raise forms.ValidationError("Invalid login")
# # class UserAccountAuthenticationForm(forms.ModelForm):
# #     email = forms.EmailField()
# #     password = forms.CharField(
# #         label="Password",
# #         strip=False,
# #         widget=forms.PasswordInput,
# #     )

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.user = None
# #         self.fields['email'].widget.attrs.update(
# #             {'placeholder': 'Enter Email'})
# #         self.fields['password'].widget.attrs.update(
# #             {'placeholder': 'Enter Password'})

# #     def clean(self, *args, **kwargs):
# #         email = self.cleaned_data.get("email")
# #         password = self.cleaned_data.get("password")

# #         if email and password:
# #             self.user = authenticate(email=email, password=password)

# #             if self.user is None:
# #                 raise forms.ValidationError("User Does Not Exist.")
# #             if not self.user.check_password(password):
# #                 raise forms.ValidationError("Password Does not Match.")
# #             if not self.user.is_active:
# #                 raise forms.ValidationError("User is not Active.")

# #         return super(UserAccountAuthenticationForm, self).clean(*args, **kwargs)

# #     def get_user(self):
# #         return self.user

#     # def clean(self, *args, **kwargs):
#     #     if self.is_valid():
#     #         email = self.cleaned_data['email']
#     #         password = self.cleaned_data['password']
#     #         if not authenticate(email=email, password=password):
#     #             raise forms.ValidationError("Invalid Login")
#     #         if self.user is None:
#     #             raise forms.ValidationError("User Does Not Exist.")
#     #         if not self.user.check_password(password):
#     #             raise forms.ValidationError("Password Does not Match.")
#     #         if not self.user.is_active:
#     #             raise forms.ValidationError("User is not Active.")
