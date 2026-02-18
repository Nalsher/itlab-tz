from django_filters import rest_framework as filters

from tag.models import Tag


class TagFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = []
