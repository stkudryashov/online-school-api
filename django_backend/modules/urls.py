from django.urls import path

from modules.views import ModuleList

app_name = 'modules'

urlpatterns = [
    path('modules', ModuleList.as_view(), name='courses'),
]
