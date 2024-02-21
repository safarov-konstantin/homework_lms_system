from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курс"
        ordering = ('name',)


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    video = models.TextField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='lesson')

    def __str__(self):
        return f'{self.name} ({self.course})'
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ('course', 'name')
