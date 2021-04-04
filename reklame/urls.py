from django.urls import path

from reklame.views import ReklameCreateView, AdvertiserReklameListView, become_advertiser, renew_subscription, \
    check_if_user_should_renew_subscription

urlpatterns = [
    path('becomeadvertiser',
         become_advertiser, name='become-advertiser'),
    path('checkifusershouldrenewsubscription', check_if_user_should_renew_subscription,
         name='check-if-user-should-renew-subscription'),
    path('publiser/new',
         ReklameCreateView.as_view(), name='reklame-create'),
    path('renewsubscription',
         renew_subscription, name='renew-subscription'),
    path('<str:username>',
        AdvertiserReklameListView.as_view(), name='advertiser-ads'),
]
