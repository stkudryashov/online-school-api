from django.db.models import Q

from accounts.models import User
from classrooms.models import Classroom, Schedule, Homework

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def get_student_courses(user: User):
    """Возвращает список словарей (course_id, course__title) курсов студента"""

    classrooms = Classroom.objects.filter(studentclassroom__student=user)
    courses = list(classrooms.values('course_id', 'course__title'))

    return courses


def get_student_lessons(user: User, module_id=None, course_id=None, wait_homework=False):
    """Возвращает список словарей (id: Schedule, lesson__title) уроков студента из расписания"""

    schedule_query = Q(classroom__studentclassroom__student=user)

    if module_id:
        schedule_query &= Q(lesson__module_id=module_id)

    if course_id:
        schedule_query &= Q(classroom__course_id=course_id)

    if wait_homework:
        schedule_query &= Q(homeworks__is_accepted=False) | Q(homeworks__isnull=True)

    schedules = Schedule.objects.filter(schedule_query)
    lessons = list(schedules.values('id', 'lesson__title'))

    return lessons


def send_student_homework(user: User, schedule_id, task_url):
    """Создает или изменяет объект домашнего задания студента"""

    try:
        validate_url = URLValidator()
        validate_url(task_url)

        schedule = Schedule.objects.get(id=schedule_id)

        homework, _ = Homework.objects.get_or_create(
            student=user,
            schedule=schedule
        )

        homework.url = task_url
        homework.save()

        return True
    except ValidationError:
        return False
