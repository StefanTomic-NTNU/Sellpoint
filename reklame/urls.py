from django.urls import path

from reklame.views import ReklameCreateView

urlpatterns = [
   # path('advertiser/<str:username>',
     #    AdvertiserReklameListView.as_view(), name='advertiser-ads'),
    #path('advertiser/<str:username>/reklame/<int:pk>/',
     #    AdvertiserReklameDetailView.as_view(), name='advertiser-ad-detail'),
    #path('reklame/<int:pk>/update',
     #    ReklameUpdateView.as_view(), name='reklame-update'),
    #path('reklame/<int:pk>/delete',
     #    ReklameDeleteView.as_view(), name='reklame-delete'),
    path('reklame/new',
         ReklameCreateView.as_view(), name='reklame-create'),
]
