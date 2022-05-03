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


class Lesson(models.Model):
    title = models.CharField(max_length=32, verbose_name='Название урока', blank=True, null=True)
    description = models.TextField(verbose_name='Описание урока', blank=True, null=True)

    document_url = models.URLField(max_length=128, verbose_name='Ссылка на документ')
    homework_url = models.URLField(max_length=128, verbose_name='Ссылка на домашнее задание')

    module = models.ForeignKey(Module, verbose_name='Модуль', on_delete=models.PROTECT,
                               related_name='lessons', blank=True, null=True)

    order_number = models.PositiveIntegerField(verbose_name='Порядок урока в модуле')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

        ordering = ['module', 'order_number']

        constraints = [
            models.UniqueConstraint(fields=['module_id', 'order_number'], name='unique_module_order'),
        ]
