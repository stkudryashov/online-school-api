from rest_framework import serializers

from accounts.models import User, UserInfo


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
