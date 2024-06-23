from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView

from .models import Dataset


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


class TaskView(LoginRequiredMixin, TemplateView):
    template_name = "task.html"


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
