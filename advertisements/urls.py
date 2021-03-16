from django.urls import path
from .views import AdvertisementListView,\
    UserAdvertisementListView, \
    AdvertisementDetailView, \
    UserAdvertisementDetailView, \
    CategoryAdvertisementDetailView, \
    CategoryAdvertisementListView, \
    AdvertisementCreateView, \
    AdvertisementUpdateView, \
    AdvertisementDeleteView, \
    advertisement_list, \
    category_list
# UserAdvertisementUpdateView, \
# CategoryAdvertisementUpdateView, \
from advertisements import views


urlpatterns = [
    # path('', views.ads, name='ads'),
    path('', advertisement_list, name='ads'),
    path('user/<str:username>', UserAdvertisementListView.as_view(), name='user-ads'),
    path('<str:category>', category_list, name='category-ads'),
    path('ad/<int:pk>/', AdvertisementDetailView.as_view(), name='ad-detail'),
    path('user/<str:username>/ad/<int:pk>/', UserAdvertisementDetailView.as_view(), name='user-ad-detail'),
    path('<str:category>/<int:pk>/', CategoryAdvertisementDetailView.as_view(), name='category-ad-detail'),
    path('ad/<int:pk>/update', AdvertisementUpdateView.as_view(), name='ad-update'),
    # path('user/<str:username>/ad/<int:pk>/update', UserAdvertisementUpdateView.as_view(), name='user-ad-update'),
    # path('<str:category>/<int:pk>/update', CategoryAdvertisementUpdateView.as_view(), name='category-ad-update'),
    path('ad/<int:pk>/delete', AdvertisementDeleteView.as_view(), name='ad-delete'),
    path('ad/new', AdvertisementCreateView.as_view(), name='ad-create')
]

