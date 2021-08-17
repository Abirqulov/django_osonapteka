from ..models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import GeometryDistance
import importlib


def get_languages(request):
    if 'lan' in request.GET:
        lan = importlib.import_module("languages." + request.GET['lan']).words
    else:
        lan = importlib.import_module("languages.ru").words

    return lan


class StoreListView(generics.ListAPIView):
    serializer_class = StoreSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ['name', 'address']
    filter_fields = ['region']
    pagination_class = None

    def get_queryset(self):
        query = Store.actives
        try:
            if 'exists' in self.request.GET and self.request.GET['exists'] == 1:
                return query.exclude(remains__isnull=False)
            lat = self.request.GET.get('lat', None)
            lng = self.request.GET.get('lng', None)

            if lat is not None and lng is not None and not lat == 'null' and not lng == 'null':
                ref_location = Point(float(lng), float(lat), srid=4326)
                return query.annotate(distance=GeometryDistance("location", ref_location)).order_by('distance')
            else:
                return query
        except KeyError:
            return query
