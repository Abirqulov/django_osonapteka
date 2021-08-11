from django.db import models
from apps.products.models import Regions, Drug
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField


# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='static/images/')
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=120)
    location = LocationField(srid=4326, geography=True, null=True, based_fields=['address'], zoom=7,
                             default=Point(41.0, 69.0))
    region = models.ForeignKey(Regions, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Remain(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.drug.name_uz + '_' + self.store.name