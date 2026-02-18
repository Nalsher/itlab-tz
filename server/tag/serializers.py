from rest_framework import serializers

from tag.models import Tag


class TagCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=64)

    class Meta:
        model = Tag
        fields = ["id", "title", "created_at"]


class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title", "created_at"]
