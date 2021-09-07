from django.db import models
from apps.products.models import Drug
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField


# Create your models here.
class Region(models.Model):
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childs', on_delete=models.DO_NOTHING)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=150)

    def __str__(self):
        return self.name_uz


class Store(models.Model):
    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.DO_NOTHING)
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120, null=True, blank=True)
    image = models.ImageField(upload_to='static/images/')
    address_uz = models.CharField(max_length=150)
    address_ru = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=120)
    location = LocationField(srid=4326, geography=True, null=True, based_fields=['address'], zoom=7, default=Point(41.0, 69.0))
    status = models.BooleanField(default=True)
    other = models.BooleanField(default=False)

    def __str__(self):
        return self.name_uz


class Remain(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, null=True, related_name='remains')
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, null=True, related_name='remains')
    qty = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    phone = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.store.name_uz