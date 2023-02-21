from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

CustomUser = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass01"
        )

        self.client.login(username="testuser", password="testpass01")
        self.tweet = Tweet.objects.create(user=self.user, content="test_tweet")

    def test_success_get(self):

        response = self.client.get(reverse("tweets:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")

        tweets = response.context["tweet_list"]
        self.assertEqual(tweets.count(), Tweet.objects.all().count())
        self.assertEqual(tweets.first().created_at, Tweet.objects.first().created_at)


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass01"
        )

        self.client.login(username="testuser", password="testpass01")

    def test_success_get(self):
        response = self.client.get(reverse("tweets:create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/create.html")

    def test_success_post(self):
        test_tweet = {"content": "testtweet"}
        response = self.client.post(reverse("tweets:create"), test_tweet)
        self.assertRedirects(
            response, reverse("tweets:home"), status_code=302, target_status_code=200
        )
        self.assertTrue(Tweet.objects.filter(content=test_tweet["content"]).exists())

    def test_failure_post_with_empty_content(self):
        empty_tweet = {"content": ""}
        response = self.client.post(reverse("tweets:create"), empty_tweet)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["content"], ["このフィールドは必須です。"])
        self.assertFalse(Tweet.objects.exists())

    def test_failure_post_with_too_long_content(self):
        too_long_tweet = {"content": "n" * 151}
        response = self.client.post(reverse("tweets:create"), too_long_tweet)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIn(
            "この値は 140 文字以下でなければなりません( {} 文字になっています)。".format(
                len(too_long_tweet["content"])
            ),
            form.errors["content"],
        )
        self.assertFalse(Tweet.objects.exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass01"
        )
        self.client.login(username="testuser", password="testpass01")
        self.tweet = Tweet.objects.create(user=self.user, content="test_tweet")

    def test_success_get(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tweet"], self.tweet)
        self.assertTemplateUsed(response, "tweets/detail.html")


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="testuser01", password="a4AXBLnb"
        )
        self.user2 = CustomUser.objects.create_user(
            username="testuser02", password="v6EaZYBT"
        )
        self.user3 = CustomUser.objects.create_user(
            username="testuser03", password="z6HqkuAR"
        )
        self.client.login(
            username="testuser01",
            password="a4AXBLnb",
        )
        self.tweet1 = Tweet.objects.create(user=self.user1, content="tweet01")
        self.tweet2 = Tweet.objects.create(user=self.user2, content="tweet02")

    def test_success_post(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet1.pk})
        )
        self.assertRedirects(response, reverse("tweets:home"), status_code=302)
        self.assertEqual(Tweet.objects.filter(content="tweet01").count(), 0)

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tweet.objects.count(), 2)

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet2.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tweet.objects.count(), 2)


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
