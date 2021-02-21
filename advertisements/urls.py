from django.urls import path
from . views import AdvertisementListView, AdvertisementDetailView
from advertisements import views


urlpatterns = [
    # path('', views.ads, name='ads'),
    path('', AdvertisementListView.as_view(), name='ads'),
    # path('ad_detail', views.ad_detail, name='ad-detail'),
    path('ad/<int:pk>/', AdvertisementDetailView.as_view(), name='ad-detail'),
]

