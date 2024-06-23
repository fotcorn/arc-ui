from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Exists, OuterRef
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, TemplateView

from .models import Dataset, Task, SolvedTask
import random


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("arc:home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("arc:home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def random_unsolved_task(request, dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)

    # Get all tasks in the dataset that haven't been solved by the user
    unsolved_tasks = Task.objects.filter(dataset=dataset).exclude(
        Exists(SolvedTask.objects.filter(task=OuterRef("pk"), user=request.user))
    )

    if unsolved_tasks.exists():
        # Get a random unsolved task efficiently
        random_task = unsolved_tasks.order_by("?").first()
    else:
        # If all tasks are solved, choose a random solved task
        solved_tasks = Task.objects.filter(
            dataset=dataset, solvedtask__user=request.user
        )
        if solved_tasks.exists():
            random_task = solved_tasks.order_by("?").first()
        else:
            # If no tasks exist in the dataset, redirect to the dataset page
            return redirect("arc:dataset", dataset_id=dataset_id)

    return redirect("arc:task", dataset_id=dataset_id, task_name=random_task.name)


class TaskView(LoginRequiredMixin, TemplateView):
    template_name = "task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dataset_id = self.kwargs["dataset_id"]
        task_name = self.kwargs["task_name"]

        dataset = get_object_or_404(Dataset, id=dataset_id)
        task = get_object_or_404(Task, dataset=dataset, name=task_name)

        context["dataset"] = dataset
        context["task"] = task
        return context


class HomeView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    context_object_name = "datasets"

    def get_queryset(self):
        return Dataset.objects.annotate(
            solved_count=Count(
                "task__solvedtask", filter=Q(task__solvedtask__user=self.request.user)
            ),
            total_count=Count("task"),
        )
