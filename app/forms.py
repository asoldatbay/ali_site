from django import forms
from django.forms import Form
from django.contrib.auth.models import User


class SignInForm(Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
