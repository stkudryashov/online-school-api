from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from accounts.models import User
from courses.models import Course

from classrooms.services import get_student_courses


def courses_list(update, user: User):
    user_courses = get_student_courses(user)

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            i.get('course__title'), callback_data=f"CourseView {i.get('course_id')}"
        ) for i in user_courses]
    )

    update.message.reply_text('Список твоих курсов 📝', reply_markup=reply_markup)


def courses_view(update, course_id):
    course = Course.objects.get(id=course_id)

    reply_markup = InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(
            module.title, callback_data=f'ModuleView {module.id}'
        ) for module in course.modules.all()] + [InlineKeyboardButton(
            'Назад', callback_data='CourseList')]
    )

    update.message.reply_text('Модули в этом курсе 📝', reply_markup=reply_markup)
