from ..models import *
from rest_framework import generics
from .serializers import *
from rest_framework.pagination import PageNumberPagination


class RegionListView(generics.ListAPIView):
    serializer_class = RegionListSerializer
    PageNumberPagination.page_size = 200

    def get_queryset(self):
        return Regions.objects.filter(parent__isnull=True).order_by('order')


class DrugListView(generics.ListAPIView):
    serializer_class = DrugSerializer
    queryset = Drug.objects.all()