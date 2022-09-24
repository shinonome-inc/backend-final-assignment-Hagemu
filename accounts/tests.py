from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import SESSION_KEY
from .models import CustumUser


class TestSignUpView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(CustumUser.objects.all().count(), 1)
        self.assertEqual(
            CustumUser.objects.filter(
                username="testuser", email="test@example.com"
            ).count(),
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
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_empty_email(self):
        data = {
            "username": "testuser",
            "email": "",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_duplicated_user(self):
        CustumUser.objects.create_user(
            username="testuser", email="test@example.com", password="Hp9My5mi"
        )
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 1)

    def test_failure_post_with_invalid_email(self):
        data = {
            "username": "testuser",
            "email": "test",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mi",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9",
            "password2": "Hp9",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testuser1",
            "password2": "testuser1",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "8131123134",
            "password2": "8131123134",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Hp9My5mi",
            "password2": "Hp9My5mm",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustumUser.objects.all().count(), 0)


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


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
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
