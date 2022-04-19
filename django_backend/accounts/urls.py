from django.urls import path

from accounts.views import RegisterAccount, ConfirmAccount, AccountInfo

from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    # Регистрация пользователя и подтверждение электронной почты
    path('user/register', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),

    # Аутентификация пользователя и обновление токена доступа
    path('user/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # Сброс пароля аккаунта
    path('user/password_reset', reset_password_request_token, name='password-reset'),
    path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),

    # Получение и редактирование информации о профиле
    path('user/profile', AccountInfo.as_view(), name='user-profile'),
]
