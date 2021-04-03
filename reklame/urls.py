from django.urls import path

from reklame.views import ReklameCreateView, AdvertiserReklameListView

urlpatterns = [
    path('<str:username>',
        AdvertiserReklameListView.as_view(), name='advertiser-ads'),
    path('publiser/new',
         ReklameCreateView.as_view(), name='reklame-create'),
]
