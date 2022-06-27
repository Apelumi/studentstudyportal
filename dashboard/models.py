from email.policy import default
from tabnanny import verbose
from tkinter import CASCADE
from turtle import width
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from matplotlib.pyplot import title

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=200)
    Description = models.TextField()

    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes"

    def __str__(self):
        return self.Title

#homwork database
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Subject = models.CharField(max_length=50)
    Title = models.CharField(max_length=50)
    Description = models.TextField()
    Due = models.DateTimeField()
    Is_Finished = models.BooleanField(default=False)

    def __str__(self):
        return self.Subject

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    Is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.Title

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todo"
    