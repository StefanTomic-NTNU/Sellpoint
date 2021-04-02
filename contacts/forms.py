from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from .models import Contact


class ContactForm(forms.ModelForm):

    message = forms.Textarea()

    class Meta:
        model = Contact
        fields = ['message']
