from django.db import models

from .utils import generate_tag_pk


# Create your models here.


class Tag(models.Model):
    id = models.CharField(primary_key=True, default=generate_tag_pk)
    title = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
