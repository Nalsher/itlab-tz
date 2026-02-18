import os

from celery import Celery

app = Celery("itlabdjango")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itlabdjango.settings")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["task"])
