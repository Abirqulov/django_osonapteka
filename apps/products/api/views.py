from ..models import *
from .serializers import *
from rest_framework import generics, filters
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DrugFilter, FullTextSearchFilterBackend
from rest_framework.settings import api_settings
from transliterate import detect_language


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializers
    queryset = Category.objects.filter(parent__isnull=True).order_by('order')


class InternationalNameListView(generics.ListAPIView):
    serializer_class = InternationalNameSerializer
    queryset = InternationalName.objects.order_by('name_uz').all()


class ManufacturerListView(generics.ListAPIView):
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.order_by('name').all()


class ReleaseFormListView(generics.ListAPIView):
    serializer_class = ReleaseFormSerializer
    queryset = ReleaseForm.objects.order_by('name_uz').all()


class DrugListView(generics.ListAPIView):
    serializer_class = DrugListSerializer
    filter_backends = (FullTextSearchFilterBackend, DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        'id': ['exact'],
        'category': ['exact'],
        'is_home': ['exact'],
        'barcode': ['exact'],
        'unit': ['exact'],
        'manufacturer': ['exact'],
    }
    filter_class = DrugFilter
    search_fields = ['#name', 'barcode']
    ordering_fields = ['name', 'price']

    def get_queryset(self):
        region_id = self.request.GET.get('region', 1)
        if len(str(region_id)) == 0:
            region_id = 1

        if 'international_name' in self.request.GET:
            search_terms = self.request.GET.get('international_name')
            if detect_language(search_terms) == 'ru':
                return Drug.products.filter(international_name__name_ru__istartswith=search_terms)
            else:
                return Drug.products.filter(international_name__name__istartswith=search_terms)

        if 'search' not in self.request.GET:
            if 'ids' in self.request.GET:
                pass
            else:
                return Drug.objects.none()

        # if region_id is None or region_id == 'null' or region_id == '':
        #     region_id = 21

        region_ids = Region.objects.filter(models.Q(parent_id=region_id) | models.Q(parent__parent_id=region_id)
                                           | models.Q(id=region_id)).values('id')

        # get_region_ids(region_id)
        drugs = Drug.products.for_region_in(region_ids)

        return drugs


class DrugDetailView(generics.RetrieveAPIView):
    serializer_class = DrugSerializer
    queryset = Drug.products.filter(status=True)