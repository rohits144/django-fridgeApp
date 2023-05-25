from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
