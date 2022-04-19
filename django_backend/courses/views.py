from rest_framework.generics import ListAPIView, RetrieveAPIView

from courses.models import Course
from courses.serializers import CourseSerializer, CourseDetailSerializer


class CourseList(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
