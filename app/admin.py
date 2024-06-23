from django.contrib import admin
from .models import Dataset, Task, SolvedTask


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "dataset")
    list_filter = ("dataset",)


@admin.register(SolvedTask)
class SolvedTaskAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "solved_date")
    list_filter = ("user", "solved_date")
    search_fields = ("task__name", "user__username")
