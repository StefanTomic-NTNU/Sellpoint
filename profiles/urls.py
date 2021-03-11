from django.urls import path

from .views import profile, ProfileDetailView

urlpatterns = [
    path('myProfile', profile, name='profile'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail')
]
