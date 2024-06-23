from django.db import models


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
