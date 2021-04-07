import random
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from reklame.models import Reklame
from .models import Advertisement, Category, UserSavedAd
from .filters import AdvertisementFilter


def advertisement_list(request):
    advertisements = Advertisement.objects.all()

    ad_filter = AdvertisementFilter(request.GET, queryset=advertisements, user=request.user)
    advertisements = ad_filter.qs

    chocen_category_id = request.GET.get('category', '')
    chocen_category_name = None
    if chocen_category_id != '':
        chocen_category_name = Category.objects.get(id=chocen_category_id).name

    saved_ads = []
    if request.user.is_authenticated:
        user_saved_ads = UserSavedAd.objects.filter(user=request.user)
        for user_saved_ad in user_saved_ads:
            saved_ads.append(user_saved_ad.ad)
    items = list(Reklame.objects.all())
    random_item = random.choice(items) if items else None
    context = {
        'advertisements': advertisements,
        'ad_filter': ad_filter,
        'logged_in_user': request.user,
        'chocen_category_name': chocen_category_name,
        'user_saved_ads': saved_ads,
        'reklame': random_item
    }
    return render(request, 'advertisements/ads.html', context)


def save_or_delete_ad(request, id):
    ad = Advertisement.objects.get(pk=id)
    try:
        user_saved_ad = UserSavedAd.objects.get(user=request.user, ad=ad)
        user_saved_ad.delete()
    except:
        UserSavedAd.objects.create(user=request.user, ad=ad)
    return redirect(request.META.get('HTTP_REFERER'))


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisements/ads.html'
    context_object_name = 'advertisements'
    ordering = ['-published']
    paginate_by = 8  # Nyttig for når vi skal implementere pagination (flere sider med ads)'


class UserAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisements/ads.html'
    context_object_name = 'advertisements'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Advertisement.objects.filter(author=user).order_by('-published')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['username'] = user.username
        items = list(Reklame.objects.all())
        random_item = random.choice(items) if items else None
        context['reklame'] = random_item
        saved_ads = []
        if self.request.user.is_authenticated:
            user_saved_ads = UserSavedAd.objects.filter(user=self.request.user)
            for user_saved_ad in user_saved_ads:
                saved_ads.append(user_saved_ad.ad)
        context['user_saved_ads'] = saved_ads
        return context


def user_saved_advertisements(request):
    user = get_object_or_404(User, username=request.user)
    user_save_ads = UserSavedAd.objects.filter(user=user)
    ads = []
    for us_ad in user_save_ads:
        ads.append(us_ad.ad)
    context = {
        'saved_ads': True,
        'advertisements': ads
    }
    return render(request, 'advertisements/ads.html', context)


class CategoryAdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisements/ads.html'
    context_object_name = 'advertisements'
    paginate_by = 8

    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return Advertisement.objects.filter(category=category).order_by('-published')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        context['category_name'] = category.name
        return context


class AdvertisementDetailView(DetailView):
    model = Advertisement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            ad = super(AdvertisementDetailView, self).get_object()
            user_saved_ad = True if UserSavedAd.objects.filter(user=user, ad=ad) else False
            context['user_saved_ad'] = user_saved_ad
            items = list(Reklame.objects.all())
            random_item = random.choice(items) if items else None
            context['reklame'] = random_item
        return context


class UserAdvertisementDetailView(DetailView):
    model = Advertisement

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        ad = super(UserAdvertisementDetailView, self).get_object()
        user_saved_ad = True if UserSavedAd.objects.filter(user=logged_user, ad=ad) else False
        context['user_saved_ad'] = user_saved_ad
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['username'] = user.username
        items = list(Reklame.objects.all())
        random_item = random.choice(items) if items else None
        context['reklame'] = random_item
        return context


class CategoryAdvertisementDetailView(DetailView):
    model = Advertisement

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        context['category_name'] = category.name
        return context


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    fields = ['title', 'description', 'price', 'category', 'latitude', 'longitude', 'image_main']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdvertisementUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView):
    model = Advertisement
    fields = ['title', 'description', 'price', 'category', 'image_main', 'latitude', 'longitude']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        advertisement = self.get_object()
        if self.request.user == advertisement.author:
            return True
        return False

    def get_success_url(self):
        # find your next url here
        next_url = self.request.POST.get('next', None)  # here method should be GET or POST.
        advertisement = self.get_object()
        if next_url:
            return advertisement.category + \
                   '/' + advertisement.id  # you can include some query strings as well
        return reverse('ads')  # what url you wish to return


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
        return False
