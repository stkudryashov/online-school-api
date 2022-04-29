from accounts.models import User
from classrooms.models import Classroom


def get_student_courses(user: User) -> list:
    """Возвращает список словарей (course_id, course__title) курсов студента"""

    classrooms = Classroom.objects.filter(studentclassroom__student=user)
    courses = list(classrooms.values('course_id', 'course__title'))

    return courses
