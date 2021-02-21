from django.urls import path
from .views import AdvertisementListView, \
    AdvertisementDetailView, \
    AdvertisementCreateView, \
    AdvertisementUpdateView, \
    AdvertisementDeleteView
from advertisements import views


urlpatterns = [
    # path('', views.ads, name='ads'),
    path('', AdvertisementListView.as_view(), name='ads'),
    # path('ad_detail', views.ad_detail, name='ad-detail'),
    path('ad/<int:pk>/', AdvertisementDetailView.as_view(), name='ad-detail'),
    path('ad/<int:pk>/update', AdvertisementUpdateView.as_view(), name='ad-update'),
    path('ad/<int:pk>/delete', AdvertisementDeleteView.as_view(), name='ad-delete'),
    path('ad/new', AdvertisementCreateView.as_view(), name='ad-create')
]

