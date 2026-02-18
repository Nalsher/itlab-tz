from task.views import TaskViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register("task", TaskViewSet, basename="task")

urlpatterns = [path("", include(router.urls))]
