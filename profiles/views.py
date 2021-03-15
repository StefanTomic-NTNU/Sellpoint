from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bruker {username} er nå registrert!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profiles/profile.html')


@login_required
def profile_confirm_delete(request):
    return render(request, 'profiles/profile_confirm_delete.html')


@login_required
def delete_user(request):
    context = {}

    try:
        u = request.user
        logout(request)
        u.delete()
        messages.success(request, f'Bruker er nå slettet!')
    except User.DoesNotExist:
        context['msg'] = 'User does not exist.'
    except Exception as e:
        context['msg'] = e.message

    return render(request, 'profiles/register.html', context=context)
