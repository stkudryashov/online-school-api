from django.db import models

from accounts.models import User
from courses.models import Course
from modules.models import Lesson


class Classroom(models.Model):
    """Модель учебной группы"""

    title = models.CharField(max_length=32, verbose_name='Название группы')

    date_start = models.DateField(blank=True, null=True, verbose_name='Дата начала учебы')
    date_end = models.DateField(blank=True, null=True, verbose_name='Дата завершения учебы')

    course = models.ForeignKey(Course, verbose_name='Название курса', on_delete=models.PROTECT,
                               related_name='classrooms', blank=True, null=True)

    mentor = models.ForeignKey(User, verbose_name='Ментор', on_delete=models.SET_NULL,
                               related_name='classrooms', blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'


class StudentClassroom(models.Model):
    """Учебная группа ученика"""

    classroom = models.ForeignKey(Classroom, verbose_name='Группа', on_delete=models.CASCADE)
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False, verbose_name='Закончил обучение')

    class Meta:
        verbose_name = 'Учебная группа ученика'
        verbose_name_plural = 'Учебные группы учеников'

        ordering = ['classroom']

        constraints = [
            models.UniqueConstraint(fields=['classroom', 'student'], name='unique_student_classroom'),
        ]


class Schedule(models.Model):
    """Расписание"""

    teacher = models.ForeignKey(User, verbose_name='Преподователь', on_delete=models.SET_NULL,
                                blank=True, null=True)
    classroom = models.ForeignKey(Classroom, verbose_name='Группа', on_delete=models.SET_NULL,
                                  blank=True, null=True)
    subject = models.ForeignKey(Lesson, verbose_name='Предмет', on_delete=models.PROTECT,
                                blank=True, null=True)
    date_of_lesson = models.DateField(blank=True, null=True, verbose_name='Дата проведения занятия')

    def __str__(self):
        return f'{self.subject.title} - {self.classroom.title}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Homework(models.Model):
    """Домашнее задание ученика"""
    homework = models.URLField(verbose_name='Ссылка на домашнее задание', max_length=200,
                               blank=True, null=True)
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE,
                                blank=True, null=True)
    date_of_publication = models.DateField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False, verbose_name='Домашняя работа выполнена верно')
    schedule = models.ForeignKey(Schedule, verbose_name='Урок', on_delete=models.CASCADE,
                                 blank=True, null=True)

    def __str__(self):
        return f'{self.schedule.title} - {self.classroom.title}'

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
