from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from task.models import Task
from user.models import User
from tag.models import Tag


# Create your tests here.


class TaskViewSetTEst(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(title="TAG")
        self.user = User.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )
        self.another_user = User.objects.create_user(
            username="testuser2", email="test2@mail.com", password="password123"
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="Test description",
            due_date=datetime.now(),
            user=self.user,
        )
        self.task.tags.add(self.tag)

    def test_viewset_requires_authentication(self):
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_list_serializer(self):
        url = reverse("task-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_detail_serializer(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_create_with_invalid_data(self):
        url = reverse("task-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data={"title": "Test Task"})
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_create_with_valid_data(self):
        url = reverse("task-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            url,
            data={
                "title": "Test Task2",
                "description": "Test description123",
                "due_date": "2020-01-01",
                "tags": ["TAG"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_delete_without_permission(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
