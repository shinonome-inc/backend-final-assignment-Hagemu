from urllib import response
from django.test import TestCase
from django.urls import reverse

from accounts.models import CustumUser


class TestHomeView(TestCase):
    def test_success_get(self):
        user = CustumUser.objects.create_user(
            username="testuser", email="test@example.com", password="Hp9My5mi"
        )
        self.client.force_login(user)
        response = self.client.get(reverse("tweets:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")


class TestTweetCreateView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_empty_content(self):
        pass

    def test_failure_post_with_too_long_content(self):
        pass


class TestTweetDetailView(TestCase):
    def test_success_get(self):
        pass


class TestTweetDeleteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
