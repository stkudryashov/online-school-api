from django.urls import path

from backend.views import RegisterAccount, ConfirmAccount

app_name = 'backend'

urlpatterns = [
    # Регистрация пользователя и подтверждение электронной почты
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
]
