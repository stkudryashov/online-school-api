from django.contrib import admin

from modules.models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass
