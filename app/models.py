from django.db import models
from django.contrib.auth.models import User


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} solved {self.task.name} on {self.solved_date}"
