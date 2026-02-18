import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_token = models.CharField(max_length=256, editable=False)
    chat_id = models.CharField(max_length=256, null=True, blank=True)

    def save(self, **kwargs):
        self.telegram_token = hashlib.sha256(self.username.encode()).hexdigest()
        super().save(**kwargs)
