from rest_framework import serializers
from .models import Task, Comment, Tag, Category


class TaskSerializer(serializers.ModelSerializer):
    # Custom field to count the number of comments on a task
    comments_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    # Custom field to count the number of tags on a task
    tags_count = serializers.IntegerField(source='tags.count', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'tags', 'comments_count', 'tags_count']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')  # or source='author.id' if you prefer

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'content', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']
