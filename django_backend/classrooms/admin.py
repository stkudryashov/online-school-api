from django.contrib import admin

from classrooms.models import Classroom, StudentClassroom


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentClassroom)
class StudentClassroomAdmin(admin.ModelAdmin):
    pass
