from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from lms_sys.models import Course, Lesson


NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_moderator(self):
        return self.groups.filter(name='moderators').exists()


class Payment(models.Model):

    date_payment = models.DateTimeField(default=timezone.now, verbose_name='дата оплаты')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='курс', default=None, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='урок', default=None, **NULLABLE)
    total = models.PositiveIntegerField(verbose_name='сумма оплаты')

    pay_method = models.CharField(
        max_length=15,
        choices=(('cash', 'наличными'), ('card', 'картой')),
        verbose_name='способ оплаты'
    )

    payment_link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)
    payment_id = models.CharField(max_length=255, verbose_name='Идентификатор платежа', unique=True, **NULLABLE)

    def __str__(self):
        return f"{self.total} {self.date_payment}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
