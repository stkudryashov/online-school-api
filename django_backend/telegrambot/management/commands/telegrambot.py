from django.core.management.base import BaseCommand

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler

from telegrambot.management.commands import keyboard

from accounts.models import User
from telegrambot.management.commands.courses import courses_view, courses_list
from telegrambot.models import BotAnswer

import logging
import telegram


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

START_LOGIN, USER_EMAIL = range(2)


def start(update: Update, context: CallbackContext):
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
    update.message.reply_text(BotAnswer.objects.get(query='Запрос почты').text)
    return USER_EMAIL


def email(update: Update, context: CallbackContext):
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
    if not User.objects.filter(telegram_id=update.message.chat_id).exists():
        start(update, context)
        return

    user = User.objects.get(telegram_id=update.message.chat_id)
    message = update.message.text

    if message == 'Личный кабинет 🖥':
        start(update, context)
    elif message == 'Мои курсы 💼':
        courses_list(update, user)
    elif message == 'Сдать работу 🎒':
        pass
    else:
        update.message.reply_text(BotAnswer.objects.get(query='Не понимаю').text)


def callbacks(update: Update, context: CallbackContext):
    button_press = update.callback_query
    user = User.objects.get(telegram_id=button_press.message.chat_id)

    if 'CourseList' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            courses_list(button_press, user)
    elif 'CourseView' in button_press.data:
        try:
            button_press.message.delete()
        except telegram.TelegramError:
            pass
        finally:
            course_id = button_press.data.split(' ')[1]
            courses_view(button_press, course_id)


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater('5340587003:AAHnwVksKrqpZuxlChoHsbbmWYqtZvkCCyA')

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

        msg_handler = MessageHandler(Filters.text & ~Filters.command, messages)
        dispatcher.add_handler(msg_handler)

        btn_handler = CallbackQueryHandler(callbacks)
        updater.dispatcher.add_handler(btn_handler)

        updater.start_polling()
        updater.idle()
