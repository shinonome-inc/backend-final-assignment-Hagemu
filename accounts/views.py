from django.contrib.auth import login
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
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result

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
