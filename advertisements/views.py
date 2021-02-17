from django.shortcuts import render

# Create your views here.


def ads(request):
    return render(request, 'advertisements/ads.html')


def single_ad(request):
    return render(request, 'advertisements/singleAd.html')
