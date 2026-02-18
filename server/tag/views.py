from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag
from tag.serializers import TagReadSerializer, TagCreateUpdateSerializer

from itlabdjango.pagination import CustomPageNumberPagination


class TagsViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    serializer_class = TagReadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["title"]
    queryset = Tag.objects.all()

    def get_serializer_class(self):
        if self.action in ("update", "create"):
            return TagCreateUpdateSerializer
        return super().get_serializer_class()
