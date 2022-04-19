from django.contrib import admin

from modules.models import Module, Lesson


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'module', 'order_number']
