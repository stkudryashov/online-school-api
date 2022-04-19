from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from rest_framework.views import APIView

from django.contrib.auth.password_validation import validate_password

from backend.serializers import UserSerializer, UserInfoSerializer, CourseSerializer, CourseDetailSerializer

from backend.signals import new_user_registered

from backend.models import ConfirmEmailToken, UserInfo, Course

from rest_framework.permissions import IsAuthenticated


class RegisterAccount(APIView):
    """Регистрация пользователя"""

    def post(self, request, *args, **kwargs):
        if {'first_name', 'last_name', 'email', 'password'}.issubset(request.data):
            try:
                # Проверка пароля на сложность
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                # Проверка на уникальность имени пользователя
                request.data._mutable = True
                request.data.update({})

                user_serializer = UserSerializer(data=request.data)

                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()

                    new_user_registered.send(sender=self.__class__, user_id=user.id)

                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ConfirmAccount(APIView):
    """Класс для подтверждения почтового адреса"""

    def post(self, request, *args, **kwargs):
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(
                user__email=request.data['email'],
                key=request.data['token']
            ).first()

            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()

                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountInfo(APIView):
    """Класс для работы с информацией пользователей"""

    permission_classes = [IsAuthenticated]

    # Получить мою информацию о профиле
    def get(self, request, *args, **kwargs):
        user_info, _ = UserInfo.objects.get_or_create(user_id=request.user.id)
        serializer = UserInfoSerializer(user_info)
        return Response(serializer.data)

    # Редактировать мою информацию о профиле
    def post(self, request, *args, **kwargs):
        print(request.data)
        if {'phone_number'}.issubset(request.data):
            user_info, _ = UserInfo.objects.get_or_create(user_id=request.user.id)

            serializer = UserInfoSerializer(user_info, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class CourseList(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
