from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

CustomUser = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]
