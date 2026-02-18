from .celery import app as celery_app
import task.tasks

__all__ = ("celery_app",)
