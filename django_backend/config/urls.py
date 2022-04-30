from django.contrib import admin
from django.urls import path, include

from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', index),

    path('admin/', admin.site.urls),

    path('api/v1/', include('accounts.urls', namespace='accounts')),
    path('api/v1/', include('courses.urls', namespace='courses')),
    path('api/v1/', include('modules.urls', namespace='modules')),
]
