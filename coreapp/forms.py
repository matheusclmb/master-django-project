from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, DateInput
from .models import City, Contact, ToDoItem


class DateInput(DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name"]
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
        }


class ToDoForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ["type", "title", "details", "urgency", "due_date"]
        widgets = {
            'due_date': DateInput(),
        }

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'