from django.urls import path

from courses.views import CourseList, CourseDetail

app_name = 'courses'

urlpatterns = [
    path('courses', CourseList.as_view(), name='courses'),
    path('courses/<int:pk>', CourseDetail.as_view(), name='course-info'),
]
