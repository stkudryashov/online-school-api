from django.contrib import admin

from courses.models import Course, CourseModule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    pass
