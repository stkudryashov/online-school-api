from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Миксин для управления пользователями"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'Admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя"""

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    email = models.EmailField(_("email address"), unique=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USER_TYPE = (
        ('student', 'Студент'),
        ('teacher', 'Учитель'),
        ('mentor', 'Ментор'),
    )

    type = models.CharField(choices=USER_TYPE, max_length=16, default='student', verbose_name='Тип пользователя')
    telegram_id = models.CharField(max_length=16, blank=True, null=True, verbose_name='Telegram ID')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)


class ConfirmEmailToken(models.Model):
    """Токен подтверждения Email"""

    @staticmethod
    def generate_key():
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
    )

    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)


class UserInfo(models.Model):
    """Информация о пользователе"""
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='user_info')

    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    phone_number_regex = RegexValidator(regex=r'^((\+7|7|8)+([0-9]){10})$')
    phone_number = models.CharField(
        validators=[phone_number_regex],
        max_length=16,
        unique=True,
        verbose_name='Номер телефона',
        blank=True, null=True
    )

    city = models.CharField(blank=True, null=True, max_length=30, verbose_name='Город')
    about_me = models.TextField(blank=True, null=True, verbose_name='Обо мне')

    def __str__(self):
        return f'{self.user.email}'

    class Meta:
        verbose_name = 'Информация о пользователе'
        verbose_name_plural = 'Информация о пользователях'
