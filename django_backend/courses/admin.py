from django.contrib import admin

from courses.models import Course, CourseModule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'module', 'order_number']
