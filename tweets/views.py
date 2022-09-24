from django.shortcuts import render

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import CustumUser

# Create your views here.


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
