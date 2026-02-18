from django.db import models
from tag.models import Tag
from .utils import generate_task_pk
from user.models import User


# Create your models here.
class Task(models.Model):
    id = models.CharField(primary_key=True, default=generate_task_pk)
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
