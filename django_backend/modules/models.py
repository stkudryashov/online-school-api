from django.db import models


class Module(models.Model):
    """Учебные модули, которыми можно наполнять различные курсы"""

    title = models.CharField(max_length=32, verbose_name='Название модуля', blank=True, null=True)
    description = models.TextField(verbose_name='Описание модуля', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
