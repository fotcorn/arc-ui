from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "arc"  # Add this line to set the namespace

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="arc:login"), name="logout"),
    path(
        "task/<int:dataset_id>/random/", views.random_unsolved_task, name="random_task"
    ),
    path(
        "task/<int:dataset_id>/<str:task_name>/", views.TaskView.as_view(), name="task"
    ),
]
