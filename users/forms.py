from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from .models import User


class UserCreationForm(CreationForm):

    class Meta(CreationForm):
        model = User
        fields = ('username', )


class UserChangeForm(ChangeForm):

    class Meta:
        model = User
        fields = ('username', )
