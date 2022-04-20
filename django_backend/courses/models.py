from django.db import models

from accounts.models import User
from modules.models import Module


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=32, verbose_name='Название курса', blank=True, null=True)
    description = models.TextField(verbose_name='Описание курса', blank=True, null=True)

    modules = models.ManyToManyField(Module, through='CourseModule', verbose_name='Модули курса')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class CourseModule(models.Model):
    """Модули на курсе с порядковыми номерами"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    module = models.ForeignKey(Module, on_delete=models.PROTECT, verbose_name='Модуль')

    order_number = models.PositiveIntegerField(verbose_name='Порядок модуля в курсе')

    def __str__(self):
        return f'{self.course.title} - {self.module.title} - {self.order_number}'

    class Meta:
        verbose_name = 'Модуль курса'
        verbose_name_plural = 'Модули курса'

        ordering = ['course', 'order_number']
