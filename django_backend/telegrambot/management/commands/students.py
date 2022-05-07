from django.utils import dateformat

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

from accounts.models import User
from classrooms.models import Schedule
from courses.models import Course
from telegrambot.models import BotAnswer

from classrooms.services import get_student_courses, get_student_lessons, send_student_homework

from telegram import Update
from telegram import ParseMode


HOMEWORK_URL = range(1)


def courses_list(update: Update.callback_query):
    """Отправляет студенту курсы, на которых он учится"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    user_courses = get_student_courses(user)

    if not user_courses:
        update.message.reply_text('Ты еще на записан на курсы 😢')
        return

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            i.get('course__title'), callback_data=f"ModulesList {i.get('course_id')}"
        ) for i in user_courses]
    )

    update.message.reply_text('Список твоих курсов 📝', reply_markup=reply_markup)


def modules_list(update: Update.callback_query, course_id):
    """Отправляет студенту модули курса, который он выбрал"""

    course = Course.objects.get(id=course_id)

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            module.title, callback_data=f'LessonsList {module.id} {course_id}'
        ) for module in course.modules.all()] + [InlineKeyboardButton('Назад ⏪', callback_data='CoursesList')]
    )

    update.message.reply_text('Модули в этом курсе 📝', reply_markup=reply_markup)


def lessons_list(update: Update.callback_query, module_id, course_id):
    """Отправляет студенту уроки из его расписания"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    user_lessons = get_student_lessons(user, module_id, course_id)

    back_button = [InlineKeyboardButton('Назад ⏪', callback_data=f'ModulesList {course_id}')]

    if not user_lessons:
        reply_markup = InlineKeyboardMarkup.from_column(back_button)
        update.message.reply_text('У тебя еще не было уроков по этому модулю 😢', reply_markup=reply_markup)
        return

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            i.get('lesson__title'), callback_data=f"LessonsView {i.get('id')} lessons_list"
        ) for i in user_lessons] + back_button
    )

    update.message.reply_text('Прошедшие уроки 📚', reply_markup=reply_markup)


def lessons_view(update: Update.callback_query, schedule_id, back_location):
    """Отправляет студенту выбранный урок (материалы, статус задания)"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    schedule = Schedule.objects.get(id=schedule_id)

    schedule_title = schedule.lesson.title.replace('.', '\.').replace('-', '\-')
    hw_status = 'Не сдано'

    message = f"*Урок:* _{schedule_title}_\n"

    keyboard = [InlineKeyboardButton('Материалы урока 📒', url=schedule.lesson.document_url)]

    if schedule.homeworks.filter(student=user).exists():
        homework = schedule.homeworks.get(student=user)

        if homework.is_accepted:
            hw_status = 'Зачтено'
        elif homework.need_to_fix:
            hw_status = 'Доработать'
            keyboard.append(InlineKeyboardButton('Исправить задание 📄', callback_data=f'HomeworksSend {schedule.id}'))
        else:
            hw_status = 'На проверке'
            keyboard.append(InlineKeyboardButton('Изменить ссылку 🔗', callback_data=f'HomeworksSend {schedule.id}'))
    else:
        keyboard.append(InlineKeyboardButton('Сдать задание 📄', callback_data=f'HomeworksSend {schedule.id}'))

    message += f'*Домашнее задание:* _{hw_status}_'

    callback_data = 'HomeworksList'

    if back_location == 'lessons_list':
        callback_data = f'LessonsList {schedule.lesson.module_id} {schedule.classroom.course_id}'

    keyboard.append(InlineKeyboardButton(text='Назад ⏪', callback_data=callback_data))

    reply_markup = InlineKeyboardMarkup.from_column(keyboard)
    update.message.reply_markdown_v2(message, reply_markup=reply_markup)


def homeworks_list(update: Update.callback_query):
    """Отправляет студенту уроки требующие сдать задание из его расписания"""

    user = User.objects.get(telegram_id=update.message.chat_id)
    user_lessons = get_student_lessons(user, wait_homework=True)

    if not user_lessons:
        update.message.reply_text('Нет заданий требующих сдачи 🥰')
        return

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            i.get('lesson__title'), callback_data=f"LessonsView {i.get('id')} homeworks_list"
        ) for i in user_lessons]
    )

    update.message.reply_text('Домашнее задание к этим урокам можно сдать 📚', reply_markup=reply_markup)


def homeworks_send(update: Update, context: CallbackContext):
    """Запрашивает ссылку на задание студента"""

    schedule_id = context.user_data.get('schedule_id')
    task_url = update.message.text

    if not schedule_id:
        update.message.reply_text('Как такое случилось? Ошибка 😢')
        return ConversationHandler.END

    user = User.objects.get(telegram_id=update.message.chat_id)
    result = send_student_homework(user, schedule_id, task_url)

    if result:
        update.message.reply_text(BotAnswer.objects.get(query='Работа отправлена').text)

        schedule = Schedule.objects.get(id=schedule_id)

        if schedule.teacher.telegram_id:
            full_name = f'{user.first_name} {user.last_name}'
            classroom = schedule.classroom.title.replace('.', '\.').replace('-', '\-')
            lesson = schedule.lesson.title.replace('.', '\.').replace('-', '\-')

            message = f'Студент *{full_name}* из группы *{classroom}* отправил домашнее задание по уроку *{lesson}* 🥰'

            context.bot.send_message(
                chat_id=schedule.teacher.telegram_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN_V2)

        return ConversationHandler.END

    update.message.reply_text(BotAnswer.objects.get(query='Неверная ссылка').text)
    return HOMEWORK_URL
