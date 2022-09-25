from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import CustomUser


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
