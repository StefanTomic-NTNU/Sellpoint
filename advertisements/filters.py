from django.db.models import Q
import django_filters as df
from django_filters import DateRangeFilter
from django_filters import RangeFilter
from django_filters.widgets import RangeWidget

from .models import Advertisement
# from .models import Category


class AdvertisementFiler(df.FilterSet):

    q = df.CharFilter(label="Søk", method='my_custom_filter')
    price = RangeFilter(label="Pris", field_name="price",
                        widget=RangeWidget(
                            attrs={'placeholder': '', 'style':"width: 10%; margin: 1%"}))

    # category = ModelChoiceFilter(label="Kategori",
    #                              field_name="category", queryset=Category.objects.all())
    published = DateRangeFilter(label='Publisert')
    ordering = df.ChoiceFilter(label='Rekkefølge', choices=(
        ('A -> Å', 'A -> Å'),
        ('Å -> A', 'Å -> A'),
        ('Dyrest øverst', 'Dyrest øverst'),
        ('Billigst øverst', 'Billigst øverst')
        ),
                               method='filter_by_order')

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