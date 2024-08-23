from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tasks.models import Task, Category, Tag, Comment
from datetime import datetime
from django.utils.timezone import make_aware

User = get_user_model()


class TaskViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Create sample categories and tags for testing
        self.category = Category.objects.create(name='Work', color='blue')
        self.tag1 = Tag.objects.create(name='Important')
        self.tag2 = Tag.objects.create(name='Urgent')

        # Create a sample task for testing
        self.task = Task.objects.create(
            title='Test Task',
            description='Task Description',
            due_date=make_aware(datetime(2024, 8, 22, 12, 0, 0)),
            category=self.category,
            author=self.user,
            status='in progress'
        )
        self.task.tags.set([self.tag1, self.tag2])

    def test_create_task(self):
        """Test creating a new task"""
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Task Description',
            'due_date': '2024-08-22T12:00:00Z',
            'category': self.category.id,
            'tags': [self.tag1.id, self.tag2.id],
            'status': 'in progress'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, 'New Task')

    def test_get_tasks(self):
        """Test retrieving tasks"""
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.task.title)

    def test_get_task_detail(self):
        """Test retrieving a single task detail"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        """Test updating a task"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {
            'title': 'Updated Task',
            'description': 'Updated Task Description',
            'due_date': '2024-08-23T12:00:00Z',
            'category': self.category.id,
            'tags': [self.tag1.id],
            'status': 'completed'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'completed')

    def test_delete_task(self):
        """Test deleting a task"""
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class CommentViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)  # Ensure the user is authenticated
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            due_date='2023-08-25T12:00:00Z',
            author=self.user
        )

        self.comment = Comment.objects.create(
            task=self.task,
            content='Test Comment',
            author=self.user
        )

    def test_create_comment(self):
        """Test creating a new comment"""
        url = reverse('comment-list')
        data = {
            'task': self.task.id,
            'content': 'New Comment Content',
        }
        response = self.client.post(url, data, format='json')

        print(response.data)  # Add this line to print the response data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(id=response.data['id']).content, 'New Comment Content')

    def test_get_comments(self):
        """Test retrieving comments"""
        url = reverse('comment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], self.comment.content)

    def test_get_comment_detail(self):
        """Test retrieving a single comment detail"""
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.comment.content)

    def test_update_comment(self):
        """Test updating a comment"""
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        data = {
            'task': self.task.id,
            'content': 'Updated Comment Content',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated Comment Content')

    def test_delete_comment(self):
        """Test deleting a comment"""
        url = reverse('comment-detail', kwargs={'pk': self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())