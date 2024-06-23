from django.contrib import admin
from .models import Dataset, Task


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "dataset")
    list_filter = ("dataset",)
