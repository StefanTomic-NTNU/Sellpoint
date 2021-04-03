from django.urls import path

from reklame.views import ReklameCreateView, AdvertiserReklameListView

urlpatterns = [
    path('<str:username>',
        AdvertiserReklameListView.as_view(), name='advertiser-ads'),
    #path('advertiser/<str:username>/reklame/<int:pk>/',
     #    AdvertiserReklameDetailView.as_view(), name='advertiser-ad-detail'),
    #path('reklame/<int:pk>/update',
     #    ReklameUpdateView.as_view(), name='reklame-update'),
    #path('reklame/<int:pk>/delete',
     #    ReklameDeleteView.as_view(), name='reklame-delete'),
    path('publiser/new',
         ReklameCreateView.as_view(), name='reklame-create'),
]
