from django.urls import path

from reklame.views import ReklameCreateView, AdvertiserReklameListView, become_advertiser, successView

urlpatterns = [
    path('becomeadvertiser',
         become_advertiser, name='become-advertiser'),
    #path('contact/', contactView, name='contact'),
    path('success/', successView, name='success'),
    path('<str:username>',
        AdvertiserReklameListView.as_view(), name='advertiser-ads'),
    path('publiser/new',
         ReklameCreateView.as_view(), name='reklame-create'),
]
