from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import CreateView

from reklame.models import Reklame


class ReklameCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reklame
    success_url = '/'
    fields = ['text', 'banner']
    success_message = 'Reklame er nå publisert!'

    def form_valid(self, form):
        form.instance.advertiser = self.request.user.profile
        return super().form_valid(form)

