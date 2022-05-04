import json

from django.db import models

from accounts.models import User
from courses.models import Course
from modules.models import Lesson

from django_celery_beat.models import PeriodicTask, ClockedSchedule

from datetime import datetime, timedelta


class Classroom(models.Model):
    """Модель учебной группы"""

    title = models.CharField(max_length=32, verbose_name='Название группы')

    date_start = models.DateField(blank=True, null=True, verbose_name='Дата начала учебы')
    date_end = models.DateField(blank=True, null=True, verbose_name='Дата завершения учебы')

    course = models.ForeignKey(Course, verbose_name='Название курса', on_delete=models.PROTECT,
                               related_name='classrooms', blank=True, null=True)

    mentor = models.ForeignKey(User, verbose_name='Ментор', on_delete=models.SET_NULL,
                               related_name='classrooms', limit_choices_to={'type': 'mentor'}, blank=True, null=True)

    is_end = models.BooleanField(default=False, verbose_name='Обучение закончено')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'


class StudentClassroom(models.Model):
    """Учебная группа ученика"""

    classroom = models.ForeignKey(Classroom, verbose_name='Группа', on_delete=models.CASCADE)
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE,
                                limit_choices_to={'type': 'student'})

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

    teacher = models.ForeignKey(User, verbose_name='Преподаватель', on_delete=models.SET_NULL,
                                limit_choices_to={'type': 'teacher'}, blank=True, null=True)

    classroom = models.ForeignKey(Classroom, verbose_name='Группа', on_delete=models.SET_NULL,
                                  related_name='schedule', blank=True, null=True)

    lesson = models.ForeignKey(Lesson, verbose_name='Урок', on_delete=models.PROTECT, blank=True, null=True)

    date_of_lesson = models.DateTimeField(blank=True, null=True, verbose_name='Дата проведения занятия')

    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)

        if ClockedSchedule.objects.filter(periodictask__name=f'Telegram Notification {self.id}').exists():
            ClockedSchedule.objects.filter(periodictask__name=f'Telegram Notification {self.id}').delete()

        clocked_schedule = ClockedSchedule.objects.create(
            clocked_time=self.date_of_lesson - timedelta(hours=1) - timedelta(hours=3)  # Костыль для scheduler
        )  # Из даты вычитаем нужный нам час до урока и еще минус три для синхронизации UTC

        PeriodicTask.objects.create(
            name=f'Telegram Notification {self.id}',
            task='telegram_notification_task',
            clocked=clocked_schedule,
            args=json.dumps([self.id]),
            one_off=True
        )

    def __str__(self):
        return f'{self.lesson.title} - {self.classroom.title}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

        ordering = ['-date_of_lesson']


class Homework(models.Model):
    """Домашнее задание ученика"""

    url = models.URLField(verbose_name='Ссылка на домашнее задание', max_length=200, blank=True, null=True)

    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE,
                                limit_choices_to={'type': 'student'}, blank=True, null=True)

    schedule = models.ForeignKey(Schedule, verbose_name='Урок', on_delete=models.CASCADE,
                                 related_name='homeworks', blank=True, null=True)

    need_to_fix = models.BooleanField(default=False, verbose_name='Требует доработки')
    is_accepted = models.BooleanField(default=False, verbose_name='Работа выполнена верно')

    date_of_publication = models.DateField(auto_now_add=True, verbose_name='Дата сдачи работы')

    def __str__(self):
        return f'{self.schedule} - {self.student.email}'

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

        constraints = [
            models.UniqueConstraint(fields=['student', 'schedule'], name='unique_student_schedule'),
        ]
