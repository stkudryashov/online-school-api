from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, ConfirmEmailToken, UserInfo


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Панель управления пользователями"""

    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')


@admin.register(UserInfo)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at')
