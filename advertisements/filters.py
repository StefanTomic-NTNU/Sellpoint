from django.db.models import Q
import django_filters as df
from django.forms import TextInput, Select
from django_filters import DateRangeFilter, CharFilter
from django_filters import ModelChoiceFilter, RangeFilter, ChoiceFilter

from .models import Advertisement
from .models import Category

from .widgets import CustomRangeWidget
from .functions import get_distance_from_lat_lon_in_km


class AdvertisementFilter(df.FilterSet):

    def __init__(self, request, queryset, user):
        super(AdvertisementFilter, self).__init__(request, queryset)
        self.user = user


    q = CharFilter(label="Søk",field_name="search", method='my_custom_filter', widget=TextInput(
                            attrs={'class' :'form-control', 'placeholder':'Søk'}))
    category = ModelChoiceFilter(label="Kategori",
                                 field_name="category", queryset=Category.objects.all(),
                                 empty_label='Velg kategori',
                                 widget=Select(
                                     attrs={'class': 'form-control'})
                                 )

    published = DateRangeFilter(label='Publisert',
                                field_name="published",
                                empty_label='Velg tidsinterval',
                                widget=Select(
                                    attrs={'class': 'form-control'})
                                )

    ordering = ChoiceFilter(label='Rekkefølge', field_name="ordering", choices=(
        ('A -> Å', 'A -> Å'),
        ('Å -> A', 'Å -> A'),
        ('Dyrest øverst', 'Dyrest øverst'),
        ('Billigst øverst', 'Billigst øverst')
        ),
                            empty_label='Velg rekkefølge',
                               method='filter_by_order',
                            widget=Select(
                                attrs={'class': 'form-control'})
                            )

    price = RangeFilter(label="Pris", field_name="price",
                        widget=CustomRangeWidget(
                            from_attrs={'placeholder': 'Pris fra'},
                            to_attrs={'placeholder': 'Pris til'},
                            attrs={'class': 'form-control'}))

    distance = ChoiceFilter(label='distance', field_name="distance", choices=(
        (0.2, 'Her (mindre enn 200m)'),
        (1, 'Veldig nært (mindre enn 1km)'),
        (3, 'Nært (mindre enn 3km)'),
        (20, 'Kjøreavstand (< 20km)')
    ),
                            empty_label='Hvor langt fra deg?',
                            method='filter_by_distance',
                            widget=Select(
                                attrs={'class': 'form-control'})
                            )

    class Meta:
        model = Advertisement
        fields = ['q']

    def my_custom_filter(self, queryset, name, value):
        return Advertisement.objects.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )

    def filter_by_order(self, queryset, name, value):
        expression = 'title'
        if value == 'Å -> A':
            expression = '-title'
        if value == 'Billigst øverst':
            expression = 'price'
        if value == 'Dyrest øverst':
            expression = '-price'
        return queryset.order_by(expression)

    def filter_by_distance(self, queryset, name, value):
        latitude = self.user.profile.latitude
        longitude = self.user.profile.longitude
        ads_ids = []
        for ad in queryset.all():
            if get_distance_from_lat_lon_in_km(ad.latitude, ad.longitude, latitude, longitude) < float(value):
                ads_ids.append(ad.id)
        return Advertisement.objects.filter(id__in=ads_ids)

