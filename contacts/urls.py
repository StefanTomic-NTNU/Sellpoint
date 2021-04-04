from django.urls import path

from .views import contact

urlpatterns = [
    path('<int:pk>/', contact, name='contact'),
]
