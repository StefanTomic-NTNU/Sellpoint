from django.urls import path

from .views import profile, my_profile, delete_user, profile_confirm_delete

urlpatterns = [
    path('myProfile', my_profile, name='profile'),
    path('<int:pk>/', profile, name='profile-detail'),
    path('confirm_delete', profile_confirm_delete, name='profile-confirm-delete'),
    path('delete', delete_user, name='profile-delete'),
]
