from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView

from reklame.models import Reklame


class ReklameCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reklame
    success_url = '/'
    fields = ['banner']
    success_message = 'Reklame er nå publisert!'

    def form_valid(self, form):
        form.instance.advertiser = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_reklames = Reklame.objects.filter(advertiser=self.request.user.profile)
        reklame_left = self.request.user.profile.reklame_limit - len(user_reklames)
        context['reklame_left'] = reklame_left
        return context


class AdvertiserReklameListView(ListView):
    model = Reklame
    template_name = 'reklame/ads.html'
    context_object_name = 'advertisements'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Reklame.objects.filter(advertiser=user.profile).order_by('-published')

