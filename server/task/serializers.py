from rest_framework import serializers

from tag.models import Tag
from tag.serializers import TagReadSerializer
from task.models import Task
from user.models import User


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField(required=False)
    due_date = serializers.DateTimeField()
    tags = serializers.SlugRelatedField(
        many=True, slug_field="title", queryset=Tag.objects.all()
    )

    def get_user(self):
        chat_id = self.context.get("request").headers.get("Chat-id")
        if chat_id:
            return User.objects.get(chat_id=chat_id)
        return self.context.get("request").user

    def create(self, validated_data):
        user = self.get_user()
        validated_data["user"] = user
        return super().create(validated_data)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "tags"]


class TaskReadSerializer(serializers.ModelSerializer):
    tags = TagReadSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "tags"]
