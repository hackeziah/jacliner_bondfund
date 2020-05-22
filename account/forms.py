from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import UserAccount, Company, Position,UserInfo


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Add a valid email address.")

    class Meta:
        model = UserAccount
        fields = ('email', 'username', 'password1', 'password2')


class CompanyForm(forms.Form):
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Company '}))

    # description = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Description'}
    # ))


class PositionForm(forms.Form):
    position_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Position '}))


class UserAccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

# class RequestForm(forms.Form):
#      emp_no = forms.CharField(required=True)
#      email = forms.EmailField(required=True)
#      balance = forms.FloatField(required=True)
#      first_name = forms.CharField(required=True)
#      last_name = forms.CharField(required=True)

#      def clean_emp_no(self):
#         try:
#             UserInfo.objects.get(emp_no__iexact = self.cleaned_data['emp_no'],trash = 0)
#         except UserInfo.DoesExist:
#             raise forms.ValidationError(("This employee number is alreaedy exist"))


# class UserAccountAuthenticationForm(forms.ModelForm):
#     email = forms.EmailField()
#     password = forms.CharField(
#         label="Password",
#         strip=False,
#         widget=forms.PasswordInput,
#     )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user = None
#         self.fields['email'].widget.attrs.update(
#             {'placeholder': 'Enter Email'})
#         self.fields['password'].widget.attrs.update(
#             {'placeholder': 'Enter Password'})

#     def clean(self, *args, **kwargs):
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         if email and password:
#             self.user = authenticate(email=email, password=password)

#             if self.user is None:
#                 raise forms.ValidationError("User Does Not Exist.")
#             if not self.user.check_password(password):
#                 raise forms.ValidationError("Password Does not Match.")
#             if not self.user.is_active:
#                 raise forms.ValidationError("User is not Active.")

#         return super(UserAccountAuthenticationForm, self).clean(*args, **kwargs)

#     def get_user(self):
#         return self.user

    # def clean(self, *args, **kwargs):
    #     if self.is_valid():
    #         email = self.cleaned_data['email']
    #         password = self.cleaned_data['password']
    #         if not authenticate(email=email, password=password):
    #             raise forms.ValidationError("Invalid Login")
    #         if self.user is None:
    #             raise forms.ValidationError("User Does Not Exist.")
    #         if not self.user.check_password(password):
    #             raise forms.ValidationError("Password Does not Match.")
    #         if not self.user.is_active:
    #             raise forms.ValidationError("User is not Active.")
