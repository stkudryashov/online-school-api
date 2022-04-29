from django.core.management.base import BaseCommand

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler

from telegrambot.management.commands import keyboard

from accounts.models import User
from telegrambot.models import BotAnswer

from telegrambot.management.commands.services import courses_list, modules_list, lessons_list, lessons_view
from telegrambot.management.commands.services import homeworks_list, homeworks_send

from telegrambot.management.commands.services import START_LOGIN, USER_EMAIL, HOMEWORK_URL

import logging
import telegram

import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')


def start(update: Update, context: CallbackContext):
    """Запускает сценарий входа в аккаунт или отправляет главное меню"""

    if User.objects.filter(telegram_id=update.message.chat_id).exists():
        update.message.reply_text(
            'Личный кабинет 🖥',
            reply_markup=keyboard.MAIN_MENU_KEYBOARD
        )

        return ConversationHandler.END

    update.message.reply_text(
        text=BotAnswer.objects.get(query='Приветствие').text,
        reply_markup=keyboard.LOGIN_BUTTON
    )

    return START_LOGIN


def login(update: Update, context: CallbackContext):
    """Запрашивает электронную почту"""

    update.message.reply_text(BotAnswer.objects.get(query='Запрос почты').text)
    return USER_EMAIL


def email(update: Update, context: CallbackContext):
    """Проверяет корректность почты, в случае успеха присваивает telegram_id"""

    user_email = update.message.text

    try:
        validate_email(user_email)

        if not User.objects.filter(email=user_email, telegram_id__isnull=True).exists():
            update.message.reply_text(BotAnswer.objects.get(query='Почта не найдена').text)
            return USER_EMAIL

        user = User.objects.get(email=user_email)

        user.telegram_id = update.message.chat_id
        user.save()

        update.message.reply_text(
            f'Добрый день, {user.first_name}!',
            reply_markup=keyboard.MAIN_MENU_KEYBOARD
        )

        return ConversationHandler.END
    except ValidationError:
        update.message.reply_text(BotAnswer.objects.get(query='Ошибка почты').text)
        return USER_EMAIL


def messages(update: Update, context: CallbackContext):
    """Обработчик текстовых сообщений от нижнего меню"""

    if not User.objects.filter(telegram_id=update.message.chat_id).exists():
        update.message.reply_text(BotAnswer.objects.get(query='Не понимаю').text)
        return

    message = update.message.text

    if message == 'Личный кабинет 🖥':
        start(update, context)
    elif message == 'Мои курсы 💼':
        courses_list(update)
    elif message == 'Сдать работу 🎒':
        homeworks_list(update)
    else:
        update.message.reply_text(BotAnswer.objects.get(query='Не понимаю').text)


def callbacks(update: Update, context: CallbackContext):
    """Обработчик inline клавиатуры под сообщениями"""

    button_press = update.callback_query

    if 'CoursesList' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            courses_list(button_press)
    elif 'ModulesList' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            course_id = button_press.data.split(' ')[1]
            modules_list(button_press, course_id)
    elif 'LessonsList' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            module_id = button_press.data.split(' ')[1]
            course_id = button_press.data.split(' ')[2]
            lessons_list(button_press, module_id, course_id)
    elif 'LessonsView' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            schedule_id = button_press.data.split(' ')[1]
            back_location = button_press.data.split(' ')[2]
            lessons_view(button_press, schedule_id, back_location)
    elif 'HomeworksList' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            homeworks_list(button_press)
    elif 'HomeworksSend' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            schedule_id = button_press.data.split(' ')[1]
            context.user_data['schedule_id'] = schedule_id
            button_press.message.reply_text('Отправь ссылку 📚')
            return HOMEWORK_URL


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(TOKEN)

        dispatcher = updater.dispatcher

        login_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                START_LOGIN: [MessageHandler(Filters.text(['Войти 🏫']), login)],
                USER_EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
            },
            fallbacks=[CommandHandler('cancel', start)],
        )
        dispatcher.add_handler(login_handler)

        homework_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(callbacks)],
            states={
                HOMEWORK_URL: [MessageHandler(Filters.text & ~Filters.command, homeworks_send)],
            },
            fallbacks=[CommandHandler('cancel', start)],
        )
        dispatcher.add_handler(homework_handler)

        msg_handler = MessageHandler(Filters.text & ~Filters.command, messages)
        dispatcher.add_handler(msg_handler)

        btn_handler = CallbackQueryHandler(callbacks)
        updater.dispatcher.add_handler(btn_handler)

        updater.start_polling()
        updater.idle()
