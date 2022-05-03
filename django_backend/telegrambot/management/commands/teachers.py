from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from accounts.models import User
from classrooms.models import Schedule
from classrooms.services import get_teacher_classrooms, get_teacher_lessons

from django.utils import dateformat

from telegram import Update


def classrooms_list(update: Update.callback_query):
    """Отправляет преподавателю группы, в которых у него есть занятия"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    user_classrooms = get_teacher_classrooms(user)

    if not user_classrooms:
        update.message.reply_text('Нет активных групп 😢')
        return

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            classroom.get('title'), callback_data=f"TeacherClassroom {classroom.get('id')}"
        ) for classroom in user_classrooms]
    )

    update.message.reply_text('Список твоих групп 👩‍🎨', reply_markup=reply_markup)


def teacher_lessons(update: Update.callback_query, classroom_id):
    """Отправляет преподавателю его занятия в выбранной группе"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    user_lessons = get_teacher_lessons(user, classroom_id)

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            lesson.get('lesson__title'), callback_data=f"TeacherLesson {classroom_id} {lesson.get('id')}"
        ) for lesson in user_lessons] + [InlineKeyboardButton('Назад ⏪', callback_data='ClassroomsList')]
    )

    update.message.reply_text('Активные занятия 💻', reply_markup=reply_markup)


def lesson_info(update: Update.callback_query, classroom_id, schedule_id):
    """Отправляет преподавателю информацию о выбранном занятии"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    schedule = Schedule.objects.get(id=schedule_id)

    title = schedule.lesson.title.replace('.', '\.')
    date = dateformat.format(schedule.date_of_lesson, 'd E')
    time = dateformat.time_format(schedule.date_of_lesson, 'H:i')

    hw_all = schedule.classroom.studentclassroom_set.all().count()
    hw_waiting = schedule.homeworks.all().count()
    hw_accepted = schedule.homeworks.filter(is_accepted=True).count()

    message = f"*Урок:* _{title}_\n"\
              f"*Дата урока:* _{date} {time}_\n\n"\
              f"*Отправили работы:* _{hw_waiting} / {hw_all}\n_"\
              f"*Получили зачет:* _{hw_accepted}_"

    back_button = [InlineKeyboardButton('Назад ⏪', callback_data=f'TeacherClassroom {classroom_id}')]
    reply_markup = InlineKeyboardMarkup.from_column(back_button)

    update.message.reply_markdown_v2(message, reply_markup=reply_markup)
