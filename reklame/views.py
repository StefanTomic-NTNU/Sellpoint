from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView, ListView
from django import forms

from reklame.models import Reklame, RequestToBeAdvertiser, RequestToRenewAbonement


def check_if_user_should_renew_subscription(request):
    reklame_left = request.user.profile.reklame_limit
    if reklame_left > 0:
        return HttpResponseRedirect(reverse('reklame-create'))
    else:
        return HttpResponseRedirect(reverse('renew-subscription'))


class ReklameCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reklame
    success_url = '/'
    fields = ['banner']
    success_message = 'Reklame er nå publisert!'

    def form_valid(self, form):
        form.instance.advertiser = self.request.user.profile
        valid = super().form_valid(form)
        if valid:
            self.request.user.profile.reklame_limit -= 1
            self.request.user.profile.save()
        return valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reklame_left = self.request.user.profile.reklame_limit
        context['reklame_left'] = reklame_left
        return context


def renew_subscription(request):
    if request.method == 'GET':
        form = forms.Form()
    else:
        form = forms.Form(request.POST)
        if form.is_valid():
            try:
                RequestToRenewAbonement.objects.create(author=request.user.profile)
            except IntegrityError:
                messages.warning(request, f'Du har allerede sendt ordre om å fornye abonementet!')
                return redirect('/')
            messages.success(request, f'Din ordre om å fornye abonementet er nå sendt!!')
            return redirect('/')
    return render(request, 'reklame/renew_subscription.html')


class AdvertiserReklameListView(ListView):
    model = Reklame
    template_name = 'reklame/ads.html'
    context_object_name = 'advertisements'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Reklame.objects.filter(advertiser=user.profile).order_by('-published')


def become_advertiser(request):
    if request.method == 'GET':
        contact_form = forms.Form()
    else:
        contact_form = forms.Form(request.POST)
        if contact_form.is_valid():
            try:
                RequestToBeAdvertiser.objects.create(author=request.user.profile)
            except IntegrityError:
                messages.warning(request, f'Du har allerede sendt en ordre om å bli annonsør!')
                return redirect('/')
            messages.success(request, f'Din ordre om å bli annonsør er nå sendt!')
            return redirect('/')
    return render(request, 'reklame/become_advertiser.html', {'contact_form': contact_form})
