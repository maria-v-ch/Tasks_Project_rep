from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            due_date='2024-12-31 23:59:59',
            author=self.user
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'Test Description')
