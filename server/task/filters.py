from django_filters import rest_framework as filters

from tag.models import Tag
from task.models import Task


class TaskFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.ModelChoiceFilter(field_name="tags", queryset=Tag.objects.all())
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    due_date = filters.DateFilter(field_name="due_date", lookup_expr="gte")

    class Meta:
        model = Task
        fields = []
