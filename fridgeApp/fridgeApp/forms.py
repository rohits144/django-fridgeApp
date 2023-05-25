from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from .widgets import DateInput
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()


class UpdateProfileForm(forms.ModelForm):

    name = forms.CharField(max_length=30)

    class Meta:
        model = Profile
        fields = ['name', 'display_pic']
        widgets = {'site_joining_date': DateInput()}

