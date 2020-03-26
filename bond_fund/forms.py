# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import authenticate
# from .models import UserAccount


# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254, help_text="Required. Add a valid email address.")

#     class Meta:
#         model = UserAccount
#         fields = ('email', 'username', 'password1', 'password2')


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
