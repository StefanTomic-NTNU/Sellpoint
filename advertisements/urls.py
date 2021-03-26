from django.urls import path
from .views import UserAdvertisementListView, \
    AdvertisementDetailView, \
    UserAdvertisementDetailView, \
    CategoryAdvertisementDetailView, \
    AdvertisementCreateView, \
    AdvertisementUpdateView, \
    AdvertisementDeleteView, \
    advertisement_list, user_saved_advertisements, save_or_delete_ad

urlpatterns = [
    path('', advertisement_list, name='ads'),
    path('user/<str:username>',
         UserAdvertisementListView.as_view(), name='user-ads'),
    path('saved',
         user_saved_advertisements, name='user-saved-ads'),
    # path('<str:category>', category_list, name='category-ads'),
    path('ad/<int:pk>/',
         AdvertisementDetailView.as_view(), name='ad-detail'),
    path('user/<str:username>/ad/<int:pk>/',
         UserAdvertisementDetailView.as_view(), name='user-ad-detail'),
    path('<str:category>/<int:pk>/',
         CategoryAdvertisementDetailView.as_view(), name='category-ad-detail'),
    path('ad/<int:pk>/update',
         AdvertisementUpdateView.as_view(), name='ad-update'),
    path('ad/<int:pk>/delete',
         AdvertisementDeleteView.as_view(), name='ad-delete'),
    path('ad/new',
         AdvertisementCreateView.as_view(), name='ad-create'),
    path('savead/<int:id>', save_or_delete_ad, name='save-or-delete-ad'),

]
