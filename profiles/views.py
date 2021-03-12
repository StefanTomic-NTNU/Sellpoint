from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.views.generic import DetailView
from .models import Profile
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



def profile(request, pk):
    own_user = request.user
    other_user = User.objects.get(pk=pk)
    return render(request, 'profiles/profile_detail.html', {'own_user':own_user, 'other_user':other_user})


@login_required
def my_profile(request):
    return profile(request, request.user.id)
    
    # return render(request, 'profiles/profile_detail.html', {'user':own_user})


# class ProfileDetailView(DetailView):
#     model = Profile
# 
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = get_object_or_404(User, pk=self.kwargs.get('pk'))
#         context['another_user'] = user
#         return context

