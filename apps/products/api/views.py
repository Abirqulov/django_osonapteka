from ..models import *
from .serializers import *
from rest_framework import generics, filters
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DrugFilter
from rest_framework.settings import api_settings


class RegionListView(generics.ListAPIView):
    serializer_class = RegionListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name_uz', 'name_ru']
    pagination_class = None

    def get_queryset(self):
        print(self.request.content_type)
        return Regions.objects.filter(parent=None)


class InternationalNameListView(generics.ListAPIView):
    serializer_class = InternationalNameSerializer
    queryset = InternationalName.objects.order_by('name_uz').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name_uz', 'name_ru']


class ManufacturerListView(generics.ListAPIView):
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.order_by('name').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name']


class ReleaseFormListView(generics.ListAPIView):
    serializer_class = ReleaseFormSerializer
    queryset = ReleaseForm.objects.order_by('name_uz').all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ['name_uz', 'name_ru']


class DrugListView(generics.ListAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name_uz', 'name_ru']


class DrugDetailView(generics.RetrieveAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name_uz', 'name_ru']
