from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Advertisement, Category
from .filters import AdvertisementFilter


def advertisement_list(request):
    advertisements = Advertisement.objects.all()

    ad_filter = AdvertisementFilter(request.GET, queryset=advertisements, user=request.user)
    advertisements = ad_filter.qs

    chocen_category_id = request.GET.get('category', '')
    chocen_category_name = None
    if chocen_category_id != '':
        chocen_category_name = Category.objects.get(id=chocen_category_id).name

    context = {
        'advertisements': advertisements,
        'ad_filter': ad_filter,
        'logged_in_user': request.user,
        'chocen_category_name': chocen_category_name
    }
    return render(request, 'advertisements/ads.html', context)


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
        return context


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

    # Code that does not work
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     uri = self.request.GET
    #     print(uri)
    #     return context


class UserAdvertisementDetailView(DetailView):
    model = Advertisement

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['username'] = user.username
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
