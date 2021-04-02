
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from profiles import views as profile_views
from django.conf import settings
from django.conf.urls.static import static
from profiles.forms import UserAuthenticationForm

urlpatterns = [
    path('', include('pages.urls')),
    path('ads/', include('advertisements.urls')),
    path('advertisements/', include('advertisements.urls')),
    path('admin/', admin.site.urls),
    path('contact/', include('contacts.urls')),
    path('profile/', include('profiles.urls')),
    path('register/', profile_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html',
                                                authentication_form=UserAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='profiles/logout.html'), name='logout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
