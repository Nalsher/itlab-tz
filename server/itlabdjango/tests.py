from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthApiViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.telegram_url = reverse("telegram-registry")

    def test_register_success(self):
        data = {
            "username": "newuser",
            "email": "newuser@mail.com",
            "password": "newpassword",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_existing_user(self):
        data = {
            "username": "testuser",
            "email": "testuser@mail.com",
            "password": "password123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_success(self):
        data = {"email": "testuser@mail.com", "password": "password123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("telegram_token", response.data)
        self.assertEqual(response.data["profile"]["username"], "testuser")

    def test_login_invalid_password(self):
        data = {"email": "testuser@mail.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_login_invalid_email(self):
        data = {"email": "wrong@mail.com", "password": "password123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_login_missing_fields(self):
        response = self.client.post(self.login_url, {"email": "", "password": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_telegram_registry_success(self):
        token = self.user.telegram_token
        chat_id = "123456789"
        response = self.client.post(
            self.telegram_url, {"token": token, "chat_id": chat_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.chat_id, chat_id)
        self.assertIn("success", response.data)

    def test_telegram_registry_invalid_token(self):
        response = self.client.post(
            self.telegram_url, {"token": "wrongtoken", "chat_id": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
