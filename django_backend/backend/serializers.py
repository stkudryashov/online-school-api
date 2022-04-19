from rest_framework import serializers

from backend.models import User, UserInfo, Course, Module


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id', 'user', 'date_of_birth', 'phone_number', 'city', 'about_me')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'title', 'description')
        read_only_fields = ('id',)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'title', 'description')
        read_only_fields = ('id',)


class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'modules')
        read_only_fields = ('id',)
