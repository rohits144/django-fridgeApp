from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Items

import datetime


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()


class AddItemForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.SelectDateWidget)
    pic = forms.ImageField(allow_empty_file=True, required=False)

    class Meta:
        model = Items
        fields = ['name', 'expiry_date', 'pic']

