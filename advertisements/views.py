from django.shortcuts import render
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


class AdvertisementDetailView(DetailView):
    model = Advertisement


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    fields = ['title', 'description', 'price', 'image_main']
    login_url = '/login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)