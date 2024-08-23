from django.test import TestCase
from tasks.models import Task, Comment, Tag, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.category = Category.objects.create(name='Work', color='blue')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            due_date='2024-12-31 23:59:59',
            author=self.user,
            category=self.category
        )

    def test_task_creation(self):
        task = Task.objects.get(title='Test Task')
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')

    def test_category_relation(self):
        self.assertEqual(self.task.category.name, 'Work')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            due_date='2024-12-31 23:59:59',
            author=self.user
        )
        self.comment = Comment.objects.create(
            content='Test Comment',
            task=self.task,
            author=self.user
        )

    def test_comment_creation(self):
        comment = Comment.objects.get(content='Test Comment')
        self.assertEqual(comment.content, 'Test Comment')
        self.assertEqual(comment.task, self.task)
