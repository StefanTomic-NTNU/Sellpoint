
from django.contrib import admin
from django.urls import path, include
from profiles import views as profile_views
from pages import views as pages_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('pages.urls')),
    path('ads/', include('advertisements.urls')),
    path('advertisements/', include('advertisements.urls')),
    path('admin/', admin.site.urls),
    path('profile/', profile_views.profile, name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
