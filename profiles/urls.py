from django.urls import path

from .views import profile, my_profile

urlpatterns = [
    path('myProfile', my_profile, name='profile'),
    path('<int:pk>/', profile, name='profile-detail')
]
