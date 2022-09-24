from django import forms
from accounts.models import CustumUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = CustumUser
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustumUser
        fields = ["username", "password"]
