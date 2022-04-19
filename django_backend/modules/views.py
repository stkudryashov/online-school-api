from django.shortcuts import render
from rest_framework.generics import ListAPIView

from modules.models import Module
from modules.serializers import ModuleSerializer


class ModuleList(ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
