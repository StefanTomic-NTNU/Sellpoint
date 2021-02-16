
from django.contrib import admin
from django.urls import path, include
from profiles import views as profile_views
from pages import views as pages_views

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('profile/', profile_views.profile, name='profile'),
    path('home/', pages_views.home, name='home')
]
