from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import TweetForm
from .models import Like, Tweet


class HomeView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = "tweets/home.html"
    queryset = Tweet.objects.select_related("user").prefetch_related("liked_tweet")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_list"] = (
            Like.objects.select_related("tweet").filter(user=self.request.user).values_list("tweet", flat=True)
        )
        return context


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/create.html"
    model = Tweet
    form_class = TweetForm
    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    template_name = "tweets/detail.html"
    model = Tweet
    queryset = Tweet.objects.select_related("user").prefetch_related("liked_tweet")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liked_list"] = (
            Like.objects.select_related("tweet")
            .filter(tweet=self.object, user=self.request.user)
            .values_list("tweet", flat=True)
        )
        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "tweets/delete.html"
    model = Tweet
    success_url = reverse_lazy("tweets:home")

    def test_func(self):
        return self.request.user == self.get_object().user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet_id = self.kwargs["pk"]
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        user = self.request.user
        Like.objects.get_or_create(tweet=tweet, user=user)
        is_liked = True
        like_url = reverse("tweets:like", kwargs={"pk": tweet_id})
        unlike_url = reverse("tweets:unlike", kwargs={"pk": tweet_id})
        like_count = tweet.liked_tweet.count()
        context = {
            "like_count": like_count,
            "tweet_id": tweet_id,
            "is_liked": is_liked,
            "like_url": like_url,
            "unlike_url": unlike_url,
        }
        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tweet_id = self.kwargs["pk"]
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        user = self.request.user
        Like.objects.filter(user=user, tweet=tweet).delete()  # 該当するLike.objectsが存在する場合のみdelete
        is_liked = False
        like_url = reverse("tweets:like", kwargs={"pk": tweet_id})
        unlike_url = reverse("tweets:unlike", kwargs={"pk": tweet_id})
        like_count = tweet.liked_tweet.count()
        context = {
            "like_count": like_count,
            "tweet_id": tweet_id,
            "is_liked": is_liked,
            "like_url": like_url,
            "unlike_url": unlike_url,
        }
        return JsonResponse(context)
