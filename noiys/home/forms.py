from .models import Comment
from django.forms import fields, widgets
from django import forms
from django.contrib.auth.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PositionForm(forms.Form):
    position = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)