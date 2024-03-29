from django.core.mail import send_mail
from celery import shared_task
from config import settings
from lms_sys.models import Course, Subscription


@shared_task
def send_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    course_sub = Subscription.objects.filter(course=course_id)
    for sub in course_sub:
        send_mail(
            subject=f"{course.name}",
            message=f"Обновление {course.name}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f'{sub.user}'],
            fail_silently=True
        )
