from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
)

from .forms import TweetForm
from .models import Tweet


class HomeView(LoginRequiredMixin, TemplateView):
    model = Tweet
    template_name = "tweets/home.html"


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/tweet_create.html"
    model = Tweet
    form_class = TweetForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        tweet = form.save(commit=False)
        tweet.user - self.request.user
        tweet.save()
        return response


class TweetDetailView(LoginRequiredMixin, DetailView):
    pass


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    pass
