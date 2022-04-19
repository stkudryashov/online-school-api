from rest_framework import serializers

from courses.models import Course
from modules.serializers import ModuleSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description')
        read_only_fields = ('id',)


class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'modules')
        read_only_fields = ('id',)
