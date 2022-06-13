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


class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    URGENCY_CHOICES = (
        ('☆', 'Low'),
        ('☆☆', 'Medium'),
        ('☆☆☆', 'High'),
        ('☆☆☆☆', 'Urgent'),
    )

    title = models.CharField(max_length=100)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=one_week_calc)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]
