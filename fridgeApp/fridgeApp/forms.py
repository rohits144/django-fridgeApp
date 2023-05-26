from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Items


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = '__all__'
