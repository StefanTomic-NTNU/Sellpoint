from django.contrib import admin
from .models import Category, UserSavedAd
from .models import Advertisement

admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(UserSavedAd)
