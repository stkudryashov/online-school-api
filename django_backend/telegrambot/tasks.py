from celery import shared_task

from django.conf import settings
from django.utils import dateformat

from accounts.models import User
from classrooms.models import Schedule

from telegram import ParseMode

import telegram


@shared_task(name='telegram_notification_task')
def telegram_notification_task(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    bot = telegram.Bot(settings.TELEGRAM_TOKEN)

    classroom = schedule.classroom.title.replace('.', '\.').replace('-', '\-')
    title = schedule.lesson.title.replace('.', '\.').replace('-', '\-')
    time = dateformat.time_format(schedule.date_of_lesson, 'H:i')

    if schedule.teacher.telegram_id:
        bot.send_message(
            chat_id=schedule.teacher.telegram_id,
            text=f'У группы *{classroom}* занятие *{title}* сегодня в *{time} МСК* 💌',
            parse_mode=ParseMode.MARKDOWN_V2
        )

    students = schedule.classroom.studentclassroom_set.all().values_list('student_id', flat=True).distinct()

    for student_id in students:
        user = User.objects.get(id=student_id)

        if user.telegram_id:
            bot.send_message(
                chat_id=user.telegram_id,
                text=f'У тебя занятие *{title}* сегодня в *{time} МСК* 💌',
                parse_mode=ParseMode.MARKDOWN_V2
            )
