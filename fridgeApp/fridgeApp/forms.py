from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Items

import datetime


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()


class AddItemForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Items
        fields = '__all__'
