from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

from mysite import settings
from tweets.models import Tweet

from .models import FriendShip

CustomUser = get_user_model()


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(
            CustomUser.objects.filter(username="testuser", email="test@example.com").count(),
            1,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")
        self.assertFormError(response, "form", "email", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password2", "このフィールドは必須です。")

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")

    def test_failure_post_with_empty_email(self):
        data = {
            "username": "testuser",
            "email": "",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "email", "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password2", "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        CustomUser.objects.create_user(username="testuser", email="test@example.com", password="Hp9My5mi")
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertFormError(response, "form", "username", "同じユーザー名が既に登録済みです。")

    def test_failure_post_with_invalid_email(self):
        data = {
            "username": "testuser",
            "email": "test",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "email", "有効なメールアドレスを入力してください。")

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9",
            "password2": "Hp9",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。")

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testuser1",
            "password2": "testuser1",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "このパスワードは ユーザー名 と似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "8131123134",
            "password2": "8131123134",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "このパスワードは数字しか使われていません。")

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mm",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "確認用パスワードが一致しません。")


class TestLoginView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="Hp9My5mi")
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        data = {"username": "testuser", "password": "Hp9My5mi"}
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        incorrect_username_data = {"username": "Vanity", "password": "Hp9My5mi"}
        response = self.client.post(self.url, incorrect_username_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            None,
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        empty_password_data = {"username": "testuser", "password": ""}
        response = self.client.post(self.url, empty_password_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password",
            "このフィールドは必須です。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser01", password="a4AXBLnb")
        self.user2 = CustomUser.objects.create_user(username="testuser02", password="v6EaZYBT")
        self.user3 = CustomUser.objects.create_user(username="testuser03", password="z6HqkuAR")
        self.client.login(
            username="testuser01",
            password="a4AXBLnb",
        )
        self.user1.following.add(self.user2)
        self.user2.following.add(self.user1)

    def test_success_get(self):
        response = self.client.get(reverse("accounts:profile", kwargs={"username": "testuser01"}))

        self.assertQuerysetEqual(response.context["tweets_list"], Tweet.objects.filter(user=self.user1))
        self.assertEqual(
            FriendShip.objects.filter(follower=self.user1).count(),
            self.user1.following.count(),
        )
        self.assertEqual(
            FriendShip.objects.filter(followee=self.user2).count(),
            self.user1.follow_by.count(),
        )


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser01", password="a4AXBLnb")
        self.user2 = CustomUser.objects.create_user(username="testuser02", password="v6EaZYBT")
        self.user3 = CustomUser.objects.create_user(username="testuser03", password="z6HqkuAR")
        self.client.login(
            username="testuser01",
            password="a4AXBLnb",
        )

    def test_success_post(self):
        response = self.client.post(reverse("accounts:follow", kwargs={"username": "testuser02"}))
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(self.user1.following.count(), 1)

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(reverse("accounts:follow", kwargs={"username": "null"}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.user1.following.count(), 0)

    def test_failure_post_with_self(self):
        response = self.client.post(reverse("accounts:follow", kwargs={"username": "testuser01"}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user1.following.count(), 0)


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser01", password="a4AXBLnb")
        self.user2 = CustomUser.objects.create_user(username="testuser02", password="v6EaZYBT")
        self.user3 = CustomUser.objects.create_user(username="testuser03", password="z6HqkuAR")
        self.client.login(
            username="testuser01",
            password="a4AXBLnb",
        )
        self.user1.following.add(self.user2)

    def test_success_post(self):
        response = self.client.post(reverse("accounts:unfollow", kwargs={"username": "testuser02"}))
        self.assertRedirects(response, reverse("tweets:home"), status_code=302, target_status_code=200)
        self.assertEqual(self.user1.following.count(), 0)

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(reverse("accounts:unfollow", kwargs={"username": "null"}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.user1.following.count(), 1)

    def test_failure_post_with_self(self):
        response = self.client.post(reverse("accounts:unfollow", kwargs={"username": "testuser01"}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.user1.following.count(), 1)


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser01", password="a4AXBLnb")
        self.client.login(
            username="testuser01",
            password="a4AXBLnb",
        )

    def test_success_get(self):
        response = self.client.get(reverse("accounts:following_list", kwargs={"username": "testuser01"}))
        self.assertEqual(response.status_code, 200)


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="testuser01", password="a4AXBLnb")
        self.client.login(
            username="testuser01",
            password="a4AXBLnb",
        )

    def test_success_get(self):
        response = self.client.get(reverse("accounts:follower_list", kwargs={"username": "testuser01"}))
        self.assertEqual(response.status_code, 200)
