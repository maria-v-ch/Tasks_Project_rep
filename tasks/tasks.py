from celery import shared_task
from django.utils import timezone
from .models import Comment, Task


@shared_task
def check_comments_for_bad_words():
    bad_words = ['bad word']  # Add more words as needed
    comments = Comment.objects.all()
    for comment in comments:
        if any(bad_word in comment.text for bad_word in bad_words):
            # Flag the comment, or take another action
            comment.is_flagged = True
            comment.save()


@shared_task
def check_task_deadlines():
    now = timezone.now()
    overdue_tasks = Task.objects.filter(due_date__lt=now, status='in_progress')
    for task in overdue_tasks:
        task.status = 'overdue'  # Or send a notification, etc.
        task.save()
