from django.contrib import admin
from .models import Reklame, RequestToBeAdvertiser, RequestToRenewAbonement

admin.site.register(Reklame)
admin.site.register(RequestToBeAdvertiser)
admin.site.register(RequestToRenewAbonement)
