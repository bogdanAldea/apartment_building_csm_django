from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from building.models import *


class CreateTenant(ModelForm):
    ...


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # fields = ['email', 'password1', 'password2']
        fields = ['username', 'email', 'password1', 'password2']


class CreateResidentialForm(ModelForm):
    class Meta:
        model = Building
        fields = '__all__'