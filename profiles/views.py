from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def register(request):
    form = UserCreationForm()
    return render(request, 'profiles/register.html', {'form': form})


def profile(request):
    return render(request, 'profiles/profile.html')
