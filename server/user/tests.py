import hashlib
from django.test import TestCase
from user.models import User


# Create your tests here.
class UserModelTest(TestCase):
    def setUp(self):
        self.username = "usernameForTest"
        self.email = "some@mail.com"
        self.password = "password12345"
        self.user = User.objects.create(
            username=self.username, email=self.email, password=self.password
        )

    def test_token_generated_incorrectly(self):
        token = hashlib.sha256("somestring".encode()).hexdigest()
        self.assertNotEqual(self.user.telegram_token, token)

    def test_token_generated_correctly(self):
        token = hashlib.sha256(self.username.encode()).hexdigest()
        self.assertEqual(self.user.telegram_token, token)
