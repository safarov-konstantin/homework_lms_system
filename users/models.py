from django.db import models
from django.contrib.auth.models import AbstractUser
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


class Payment(models.Model):
     
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='пользователь')
    date_payment = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name='курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, verbose_name='урок')
    total = models.FloatField(verbose_name='сумма оплаты')
   
    pay_method = models.CharField(
        max_length=15,
        choices=(('cash', 'наличными'), ('card', 'картой')),
        verbose_name='способ оплаты'
    )

    def __str__(self):
        return f"{self.user} {self.date_payment}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежы"
