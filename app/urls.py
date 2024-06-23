from django.urls import path
from . import views

app_name = "arc"  # Add this line to set the namespace

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("task/", views.TaskView.as_view(), name="task"),
]
