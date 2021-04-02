import random

from django.shortcuts import render
from django.http import HttpResponse
from advertisements.models import Category
from reklame.models import Reklame


def home(request):
    items = list(Reklame.objects.all())
    random_item = random.choice(items) if items else None
    context = {
        'categories': Category.objects.all(),
        'reklame': random_item
    }
    return render(request, 'pages/home.html', context)
