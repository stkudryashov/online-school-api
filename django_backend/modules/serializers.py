from rest_framework import serializers

from modules.models import Module, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'module', 'title', 'description', 'document_url', 'homework_url', 'teacher', 'order_number')
        read_only_fields = ('id',)
        extra_kwargs = {
            'module': {'write_only': True}
        }


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)

    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'lessons')
        read_only_fields = ('id',)
