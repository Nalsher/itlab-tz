from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tag.models import Tag
from user.models import User


class TagsViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@mail.com", password="password123"
        )
        self.tag1 = Tag.objects.create(title="Tag 1")
        self.tag2 = Tag.objects.create(title="Tag 2")

    def test_tag_list_requires_authentication(self):
        url = reverse("tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tag_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_create_with_valid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tag-list")
        response = self.client.post(url, data={"title": "New Tag"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tag_create_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("tag-list")
        response = self.client.post(url, data={"title": ""})
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
