import django_filters

from shopapp.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", method="name_filter")
    # price = django_filters.NumberFilter()
    # price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label="filter[minPrice]")
    # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label="filter[maxPrice]")
    #

    class Meta:
        model = Product
        fields = ["name", "price"]

    def name_filter(self, queryset, name, value):
        pass
