from django.urls import path
from advertisements import views


urlpatterns = [
    path('', views.ads, name='ads'),
    path('ad_detail', views.ad_detail, name='ad-detail'),
]

