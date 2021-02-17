from django.shortcuts import render

# Create your views here.


def ads(request):
    return render(request, 'advertisements/ads.html')


def ad_detail(request):
    return render(request, 'advertisements/ad_detail.html')
