from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'complete', 'created')
    list_filter = ('user', 'complete')
    search_fields = ('title', 'description')
