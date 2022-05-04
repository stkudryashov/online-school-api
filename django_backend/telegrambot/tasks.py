from celery import shared_task
from django.conf import settings

from accounts.models import User

import telegram


@shared_task(name='telegram_notification_task')
def telegram_notification_task(schedule_id=None):
    user = User.objects.get(email='aleks59niki30@gmail.com')

    bot = telegram.Bot(settings.TELEGRAM_TOKEN)
    bot.send_message(chat_id=user.telegram_id, text='Работает!')
