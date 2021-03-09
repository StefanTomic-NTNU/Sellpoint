from django.shortcuts import render
from django.http import HttpResponse
from advertisements.models import Category

def home(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'pages/home.html', context)

