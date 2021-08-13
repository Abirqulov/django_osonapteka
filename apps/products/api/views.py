from ..models import *
from rest_framework import generics
from .serializers import *
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DrugFilter


class RegionListView(generics.ListAPIView):
    serializer_class = RegionListSerializer
    PageNumberPagination.page_size = 200

    def get_queryset(self):
        return Regions.objects.filter(parent__isnull=True).order_by('order')


class InternationalNameListView(generics.ListAPIView):
    serializer_class = InternationalNameSerializer
    queryset = InternationalName.objects.order_by('name_uz').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name_uz', 'name_ru']


class ManufacturerListView(generics.ListAPIView):
    serializer_class = ManufactureSerializer
    queryset = Manufacturer.objects.order_by('name_uz').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name_uz', 'name_ru']


class ReleaseFormListView(generics.ListAPIView):
    serializer_class = ReleaseFormSerializer
    queryset = Manufacturer.objects.order_by('name_uz').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name_uz', 'name_ru']

#
# class DrugListView(generics.ListAPIView):
#     serializer_class = DrugSerializer
#     queryset = Drug.objects.all()
