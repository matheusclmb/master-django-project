from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


def one_week_calc():
    return timezone.now() + timezone.timedelta(days=7)


class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class ToDoItem(models.Model):
    URGENCY_CHOICES = (
        ('☆', 'Low'),
        ('☆☆', 'Medium'),
        ('☆☆☆', 'High'),
        ('☆☆☆☆', 'Urgent'),
    )

    type = models.CharField(max_length=25, default="Default")
    title = models.CharField(max_length=100)
    details = models.TextField(max_length=500, blank=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=one_week_calc)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["due_date"]


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

