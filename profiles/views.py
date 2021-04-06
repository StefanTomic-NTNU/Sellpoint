from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse

from .models import Feedback, Profile
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from sellpoint import settings
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, FeedbackForm, FeedbackUpdateForm


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
    return render(request, 'profiles/profile_detail.html', {'own_user': own_user, 'other_user': other_user})


@login_required
def my_profile(request):
    return profile(request, request.user.id)


@login_required
def profile_confirm_delete(request):
    return render(request, 'profiles/profile_confirm_delete.html')


def profile_delete(request):
    """
    Deletes profile, which cascades to user.
    No login_required annotation is needed because
    the check is performed in the function. This
    is to avoid the user being redirected to
    /profiles/delete when logging in after
    trying to access the url when logged out.
    """
    context = {}

    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)

    try:
        u = request.user
        logout(request)
        u.delete()
        messages.success(request, f'Din bruker er nå slettet!')
    except User.DoesNotExist:
        context['msg'] = 'User does not exist.'
    except Exception as e:
        context['msg'] = e.message

    return render(request, 'profiles/register.html', context=context)


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profilen din er oppdatert!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profiles/profile_update.html', context)


class FeedbackListView(ListView):
    model = Feedback
    template_name = 'profiles/feedback_list.html'
    ordering = ['published']

    def get(self, request, pk):
        own_user = request.user
        other_user = User.objects.get(pk=pk)
        object_list = Feedback.objects.all().filter(recipient=other_user.id)
        return render(request, 'profiles/feedback_list.html', {
            'own_user': own_user,
            'other_user': other_user,
            'object_list': object_list,
        })


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'profiles/feedback_create.html'

    def post(self, request, pk):
        author = request.user
        recipient = User.objects.get(pk=pk)
        recipient_profile = Profile.objects.get(user=recipient)
        form_temp = FeedbackForm(request.POST)
        form = form_temp.save(commit=False)
        form.author = author
        form.recipient = recipient_profile
        form.save()
        return HttpResponseRedirect('/profile/' + str(recipient.id) + '/feedback/')

    def form_valid(self, form):
        form.instance.feedback_id = self.kwargs['pk']
        return super().form_valid(form)


class DeleteFeedbackView(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'profiles/feedback_delete.html'

    def get(self, request, pk):
        recipient_feedback = Feedback.objects.get(pk=pk)
        recipient = recipient_feedback.recipient
        return render(request, 'profiles/feedback_delete.html', {
            'recipient': recipient,
        })

    def delete(self, request, pk):
        recipient_feedback = Feedback.objects.get(pk=pk)
        recipient = recipient_feedback.recipient
        recipient_feedback.delete()
        return HttpResponseRedirect('/profile/' + str(recipient.id) + '/feedback/')


class UpdateFeedbackView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    template_name = 'profiles/feedback_update.html'
    form_class = FeedbackUpdateForm

    def form_valid(self, form):
        form.instance.feedback_id = self.kwargs['pk']
        form.save()
        return super().form_valid(form)

    def test_func(self):
        feedback = self.get_object()
        if self.request.user == feedback.author:
            return True
        return False

    def post(self, request, pk):
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            recipient_feedback = Feedback.objects.get(pk=pk)
            recipient = recipient_feedback.recipient
            if form.is_valid():
                obj = Feedback()
                obj.comment = form.cleaned_data['comment']
                obj.rating = form.cleaned_data['rating']
                obj.save()
        return HttpResponseRedirect('/profile/' + str(recipient.id) + '/feedback/')

