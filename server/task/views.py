from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from task.models import Task
from task.serializers import TaskReadSerializer, TaskCreateUpdateSerializer
from user.models import User
from task.tasks import due_date_notify
from itlabdjango.pagination import CustomPageNumberPagination
from task.filters import TaskFilterSet


class TaskViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    serializer_class = TaskReadSerializer
    queryset = Task.objects.all().order_by("created_at")
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["title"]
    filterset_class = TaskFilterSet

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return TaskCreateUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.get_user()
        return super().get_queryset().filter(user=user)

    def get_user(self):
        if self.request.user.is_authenticated:
            return self.request.user
        chat_id = self.request.headers.get("Chat-id")
        if not chat_id:
            raise PermissionDenied("No telegram chat_id provided")
        try:
            return User.objects.get(chat_id=chat_id)
        except User.DoesNotExist:
            raise PermissionDenied("No such user exists")

    def check_permissions(self, request):
        user = self.get_user()
        if not user:
            super().check_permissions(request)

    def has_object_permissions(self, request, view, obj):
        user = self.get_user()
        if obj.user != user:
            raise PermissionDenied("You cannot modify this task")
        return True

    def get_object(self):
        obj = super().get_object()
        self.has_object_permissions(self.request, self, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)

        if instance.user.chat_id:
            due_date_notify.apply_async(
                args=(instance.user.chat_id, instance.title), eta=instance.due_date
            )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
