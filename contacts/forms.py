from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):

    message = forms.Textarea()

    phone = forms.CharField()

    email = forms.EmailField()

    class Meta:
        model = Contact
        fields = ['message', 'phone', 'email']
