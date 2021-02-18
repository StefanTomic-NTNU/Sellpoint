from django.shortcuts import render
from .models import Advertisement


def ads(request):
    context = {
        'advertisements': Advertisement.objects.all()
    }
    return render(request, 'advertisements/ads.html', context)


def ad_detail(request):
    return render(request, 'advertisements/ad_detail.html')
