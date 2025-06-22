from celery import shared_task
from .models import Story
from django.utils import timezone
from datetime import timedelta

@shared_task
def delete_stories():
    stories = Story.objects.filter(created_at__lt=timezone.now() - timedelta(hours=12))
    stories.delete()