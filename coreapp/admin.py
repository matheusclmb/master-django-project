from django.contrib import admin
from .models import City, ToDoList, ToDoItem

# Register your models here.
admin.site.register(City)
admin.site.register(ToDoList)
admin.site.register(ToDoItem)
