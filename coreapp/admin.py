from django.contrib import admin
from .models import City, ToDoItem, Contact

# Register your models here.
admin.site.register(City)
admin.site.register(ToDoItem)
admin.site.register(Contact)