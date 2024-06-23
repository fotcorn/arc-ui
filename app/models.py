from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class ARCUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class ARCUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ARCUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Dataset(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.TextField()
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    train = models.JSONField()
    test = models.JSONField()

    def __str__(self):
        return self.name


class SolvedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    solved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} solved {self.task.name} on {self.solved_date}"
