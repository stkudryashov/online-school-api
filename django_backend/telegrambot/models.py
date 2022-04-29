from django.db import models


class BotAnswer(models.Model):
    """Ответы для Telegram бота"""

    query = models.CharField(max_length=32, verbose_name='Название ответа')
    text = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.query}'

    class Meta:
        verbose_name = 'Ответ бота'
        verbose_name_plural = 'Ответы бота'
