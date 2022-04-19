from django.contrib import admin

from classrooms.models import Classroom, StudentClassroom, Schedule, Homework


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'mentor', 'date_start', 'date_end']


@admin.register(StudentClassroom)
class StudentClassroomAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'student', 'is_completed']
    search_fields = ['classroom__title', 'student__email']

