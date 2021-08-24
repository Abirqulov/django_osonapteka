from django_filters import Filter, FilterSet, filters
from rest_framework.compat import distinct
from rest_framework import filters as r_filters
from transliterate import translit
from ..models import *
import operator
from functools import reduce
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity


class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class SearchFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'icontains'
        return super(SearchFilter, self).filter(qs, value)


class FullTextSearchFilterBackend(r_filters.SearchFilter):
    def __init__(self):
        self.lookup_prefixes['#'] = 'trigram_similar'
        self.lookup_prefixes['~'] = 'unaccent'

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]
        base = queryset
        conditions = []

        for search_term in search_terms:
            queries = []

            for orm_lookup in orm_lookups:

                if orm_lookup == 'name__trigram_similar':
                    search_terms = ' '.join(search_terms)
                    search_terms = translit(search_terms, 'ru')
                    if queryset.filter(name__istartswith=search_terms).count() > 0:
                        queryset = queryset.filter(Q(name__istartswith=search_terms),)

                    if queryset.filter(barcode__contains=search_terms).count() > 0:
                        queryset = queryset.filter(Q(barcode__contains=search_terms), )

                    else:
                        queryset = queryset.annotate(similarity=TrigramSimilarity('name', search_terms), ).filter(
                            Q(name__icontains=search_term) | Q(similarity__gt=0.16)
                        ).order_by('-similarity')

                    return queryset
                else:
                    queries += [
                        Q(**{orm_lookup: search_term})
                    ]

            conditions.append(reduce(operator.or_, queries))

        queryset = queryset.filter(reduce(operator.and_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            queryset = distinct(queryset, base)
        return queryset


class DrugFilter(FilterSet):
    ids = ListFilter(field_name='id')
    international_name_ids = ListFilter(field_name='international_name_id')
    manufacturer_ids = ListFilter(field_name='manufacturer_id')
    unit_ids = ListFilter(field_name='unit_id')
    is_home = filters.NumberFilter(field_name='is_home')
    category = filters.NumberFilter(field_name='category')
    barcode = filters.CharFilter(field_name='barcode')
    slug = filters.CharFilter(field_name='slug')
    price = filters.RangeFilter(field_name='price')

    class Meta:
        model = Drug
        fields = [
            'ids',
            'category',
            'is_home',
            'barcode',
            'price',
            'unit_ids',
            'manufacturer_ids',
            'international_name_ids',
            'slug',
        ]

