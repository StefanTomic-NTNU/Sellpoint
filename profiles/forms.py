from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        self.error_messages['password_mismatch'] = 'De to passordfeltene stemmer ikke overens'
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username__iexact=username)
        if users:
            raise forms.ValidationError("Brukernavnet er allerede registrert.")
        return username

    email = forms.EmailField(
        label="Email"
    )
    username = UsernameField(
        label='Brukernavn',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password1 = forms.CharField(
        label='Passord',
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label='Bekreft passord',
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = \
            'Vennligst skriv inn riktig ' \
            'brukernavn og passord. ' \
             'Merk at begge feltene kan ' \
             'være store og små bokstaver.'
        super().__init__(*args, **kwargs)

    username = UsernameField(
        label='Brukernavn',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password = forms.CharField(
        label='Passord',
        strip=False,
        widget=forms.PasswordInput,
    )

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
