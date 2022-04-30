from telegram import ReplyKeyboardMarkup


LOGIN_BUTTON = ReplyKeyboardMarkup.from_button(
        button='Войти 🏫',
        resize_keyboard=True,
        one_time_keyboard=True
    )


STUDENT_MENU_KEYBOARD = ReplyKeyboardMarkup.from_column(
    button_column=['Мои курсы 💼', 'Сдать работу 🎒'],
    resize_keyboard=True,
)


TEACHER_MENU_KEYBOARD = ReplyKeyboardMarkup.from_column(
    button_column=['Мои студенты 🧑🏼‍🎓', 'Уведомить студентов ☎️'],
    resize_keyboard=True,
)
