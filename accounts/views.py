from django.contrib.auth import authenticate, login
from django.views.generic import CreateView

from .forms import SignupForm
from .models import CustomUser


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

    # class LoginView(LoginView):
    pass

    # class LogoutView(LogoutView):
    pass

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
