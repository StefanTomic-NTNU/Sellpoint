from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Advertisement


def ads(request):
    context = {
        'advertisements': Advertisement.objects.all()
    }
    return render(request, 'advertisements/ads.html', context)

#
# def ad_detail(request):
#     return render(request, 'advertisements/advertisement_detail.html')


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisements/ads.html'
    context_object_name = 'advertisements'
    ordering = ['-published']    # Forteller at annonsene skal være sortert nyest-eldst publisert'
    paginate_by = 8     # Nyttig for når vi skal implementere pagination (flere sider med ads)'


class UserAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisements/user_ads.html'
    context_object_name = 'advertisements'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Advertisement.objects.filter(author=user).order_by('-published')


class AdvertisementDetailView(DetailView):
    model = Advertisement


class UserAdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'advertisements/user_advertisement_detail.html'


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    fields = ['title', 'description', 'price', 'image_main']
    labels = {      # Dette gjør ingenting atm..
        'title':'Tittel',
        'description':'Beskrivelse',
        'price':'Pris',
        'image_main':'Bilde',
    }
    login_url = '/login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdvertisementUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView):

    model = Advertisement
    fields = ['title', 'description', 'price', 'image_main']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        advertisement = self.get_object()
        if self.request.user == advertisement.author:
            return True
        else:
            return False


class AdvertisementDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView):

    model = Advertisement
    success_url = '/ads'

    def test_func(self):
        advertisement = self.get_object()
        if self.request.user == advertisement.author:
            return True
        else:
            return False

