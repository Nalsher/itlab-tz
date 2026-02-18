from tag.views import TagsViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register("tag", TagsViewSet, basename="tag")

urlpatterns = [path("", include(router.urls))]
