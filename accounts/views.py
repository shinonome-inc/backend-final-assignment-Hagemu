from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView, TemplateView

from tweets.models import Tweet

from .forms import LoginForm, SignupForm
from .models import CustomUser, FriendShip


class WelcomeView(CreateView):
    pass


class SignUpView(CreateView):
    model = CustomUser
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = "/tweets/home/"

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class LogoutView(LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/profile.html"
    model = Tweet
    context_object_name = "tweets_list"

    def get_queryset(self):
        return (
            Tweet.objects.select_related("user")
            .filter(user__username=self.kwargs.get("username"))
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        user = get_object_or_404(CustomUser, username=self.kwargs["username"])
        context = super().get_context_data(**kwargs)
        context["username"] = user.username
        context["following_now"] = self.request.user.following.filter(
            username=user.username
        ).exists()
        context["following_count"] = FriendShip.objects.filter(follower=user).count()
        context["follower_count"] = FriendShip.objects.filter(followee=user).count()
        return context


class FollowView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("tweets:home")

    def post(self, request, *args, **kwargs):
        target_user = get_object_or_404(CustomUser, username=self.kwargs["username"])
        if target_user == self.request.user:
            messages.add_message(request, messages.ERROR, "自分自身をフォローすることはできません。")
            return HttpResponseBadRequest("you cannnot follow yourself.")
        elif self.request.user.following.filter(username=target_user.username).exists():
            messages.add_message(request, messages.INFO, "既にフォローしています。")
        else:
            self.request.user.following.add(target_user)
            messages.add_message(request, messages.SUCCESS, "フォローしました。")
        return super().post(request, *args, **kwargs)


class UnFollowView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("tweets:home")

    def post(self, request, *args, **kwargs):
        target_user = get_object_or_404(CustomUser, username=self.kwargs["username"])
        if target_user == self.request.user:
            messages.add_message(request, messages.ERROR, "自分自身をフォロー解除することはできません。")
            return HttpResponseBadRequest("you cannot unfollow yourself.")
        elif self.request.user.following.filter(username=target_user.username).exists():
            self.request.user.following.remove(target_user)
            messages.add_message(request, messages.SUCCESS, "フォロー解除しました。")
        else:
            messages.add_message(request, messages.INFO, "このユーザーをフォローしていません。")
        return super().post(request, *args, **kwargs)


class FollowingListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/following_list.html"

    def get_context_data(self, **kwargs):
        target_user = get_object_or_404(
            CustomUser,
            username=self.kwargs.get("username"),
        )
        context = super().get_context_data(**kwargs)
        context["following_list"] = target_user.follower.order_by("-created_at")
        return context


class FollowerListView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follower_list.html"

    def get_context_data(self, **kwargs):
        target_user = get_object_or_404(
            CustomUser,
            username=self.kwargs.get("username"),
        )
        context = super().get_context_data(**kwargs)
        context["follower_list"] = target_user.followee.order_by("-created_at")
        return context
