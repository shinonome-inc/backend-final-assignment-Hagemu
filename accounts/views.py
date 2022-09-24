from django.shortcuts import render
from django.contrib.auth import login

from .forms import SignupForm, LoginForm
from .models import CustumUser

# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class WelcomeView(CreateView):
    pass


class SignUpView(CreateView):
    model = CustumUser
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = "/tweets/home/"

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(LogoutView):
    template_name = "accounts/logout.html"


# class UserProfileView(LoginRequiredMixin, TemplateView):
    pass

    # class TweetCreateView(request):
    pass

    # class TweetDetailView(request):
    pass

    # class TweetDeleteView(request):
    pass

    # class LikeView(request):
    pass

    # class UnlikeView(request):
    pass

    # class FollowView(request):
    pass

    # class UnfollowView(request):
    pass

    # class FollowingListView(request):
    pass

    # class FollowerListView(request):
    pass
