from .serializers import *
from django_filters import Filter, FilterSet, filters


class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class DrugFilter(FilterSet):
    ids = ListFilter(field_name='id')
    international_name_ids = ListFilter(field_name='international_name_id')
    manufacturer_ids = ListFilter(field_name='manufacturer_id')
    release_form_ids = ListFilter(field_name='release_form_id')
    is_home = filters.NumberFilter(field_name='is_home')
    region_slug = filters.CharFilter(field_name='region_slug')
    region = filters.NumberFilter(field_name='region')
    barcode = filters.CharFilter(field_name='barcode')
    price = filters.RangeFilter(field_name='price')

    class Meta:
        model = Drug
        fields = [
            'ids',
            'region',
            'region_slug',
            'is_home',
            'barcode',
            'price',
            'manufacturer_ids',
            'international_name_ids',
            'release_form_id',
        ]

    @property
    def qs(self):
        parent = super().qs

        if not parent:
            region_slug = self.request.GET.get('category_slug')
            region = self.request.GET.get('region', 1)

            if region_slug:
                regions = Regions.objects.filter(slug=region_slug).first().childs.all()
                parent = Drug.products.filter(category__in=regions, drugs_price__region_id=region)

        return parent
