from telegram import Update
from telegram.ext import CallbackContext

from accounts.models import User

from telegrambot.management.commands import keyboard
from telegrambot.models import BotAnswer


def get_user_keyboard(user: User):
    if user.type == 'teacher':
        return keyboard.TEACHER_MENU_KEYBOARD
    else:
        return keyboard.STUDENT_MENU_KEYBOARD


def change_user_type(update: Update, context: CallbackContext):
    if not User.objects.filter(telegram_id=update.message.chat_id).exists():
        update.message.reply_text(BotAnswer.objects.get(query='Не понимаю').text)
        return

    user = User.objects.get(telegram_id=update.message.chat_id)

    if user.is_superuser:
        if context.args:
            new_type = context.args[0]

            if new_type not in [user_type[0] for user_type in User.USER_TYPE]:
                update.message.reply_text('Неверный тип пользователя 🥲')
            else:
                user.type = new_type
                user.save()

                update.message.reply_text(
                    'Успешно ❤️',
                    reply_markup=get_user_keyboard(user)
                )
        else:
            update.message.reply_markdown_v2(f'Тип аккаунта: `{user.type}`')
    else:
        update.message.reply_text(BotAnswer.objects.get(query='Не понимаю').text)
