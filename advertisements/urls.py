from django.urls import path
from advertisements import views


urlpatterns = [
    path('', views.ads, name='ads'),
    path('single_ad', views.single_ad, name='single-ad')
]

