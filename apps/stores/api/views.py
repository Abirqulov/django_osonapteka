from ..models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import GeometryDistance


class StoreListView(generics.ListAPIView):
    serializer_class = StoreSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name', 'address']
    filter_fields = ['region']
    pagination_class = None

    def get_queryset(self):
        query = Store.objects.filter(status=True)
        try:
            if 'exists' in self.request.GET and self.request.GET['exists'] == 1:
                return query.exclude(remains__isnull=True)
            lat = self.request.GET.get('lat', None)
            lng = self.request.GET.get('lng', None)
            if lat is not None and lng is not None:
                ref_location = Point(float(lng), float(lat), srid=4326)
                return query.annotate(distance=GeometryDistance("location", ref_location)).order_by('distance')
            else:
                return query
        except KeyError:
            return query


class RegionListView(generics.ListAPIView):
    serializer_class = RegionListSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name']

    def get_queryset(self):
        queryset = Region.objects.filter(Q(parent=None) | Q(parent=1)).order_by('id')
        return queryset
