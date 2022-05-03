from datetime import datetime, timedelta

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
        schedule_query &= Q(homeworks__is_accepted=False, homeworks__need_to_fix=True) | Q(homeworks__isnull=True)

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
        homework.need_to_fix = False

        homework.save()

        return True
    except ValidationError:
        return False


def get_student_schedule(user: User, view_range=None):
    """Возвращает список словарей (lesson__title, date_of_lesson) расписания студента"""

    schedule_query = Q(classroom__studentclassroom__student=user)

    if view_range:
        schedule_query &= Q(date_of_lesson__gte=datetime.now() - timedelta(hours=2))
        schedule_query &= Q(date_of_lesson__lte=datetime.now() + timedelta(days=view_range))

    schedule = Schedule.objects.filter(schedule_query).values('lesson__title', 'date_of_lesson').distinct()

    return schedule


def get_teacher_classrooms(user: User):
    """Возвращает список словарей (id, title) учебных групп учителя"""

    classrooms = list(Classroom.objects.filter(schedule__teacher=user, is_end=False).values('id', 'title').distinct())

    return classrooms


def get_teacher_lessons(user: User, classroom_id):
    """Возвращает список словарей (id: Schedule, lesson__title) занятий преподавателя в выбранной группе"""

    classroom = Classroom.objects.get(id=classroom_id)
    lessons = list(classroom.schedule.filter(teacher=user).values('id', 'lesson__title'))

    return lessons
