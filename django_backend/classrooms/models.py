from django.db import models

from accounts.models import User
from courses.models import Course


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

    def __str__(self):
        return f'{self.classroom.title} - {self.student.email}'

    class Meta:
        verbose_name = 'Учебная группа ученика'
        verbose_name_plural = 'Учебные группы учеников'

        ordering = ['classroom']

        constraints = [
            models.UniqueConstraint(fields=['classroom', 'student'], name='unique_student_classroom'),
        ]
