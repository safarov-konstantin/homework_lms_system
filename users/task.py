from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from celery import shared_task


@shared_task
def check_last_data():
    user = get_user_model()
    deadline_data = timezone.now() - timedelta(days=30)
    inactive_users = user.objects.filter(last_login__lt=deadline_data, is_active=True)
    inactive_users.update(is_active=False)
    print(f'Deactivated {inactive_users.count()} users')
