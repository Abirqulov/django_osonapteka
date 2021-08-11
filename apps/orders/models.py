from django.db import models
from account.models import User
from apps.products.models import Drug
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='myorders')
    phone = models.CharField(max_length=120)
    address = models.CharField(max_length=150)
    location = LocationField(srid=4326, geography=True, null=True, based_fields=['address'], zoom=7, default=Point(41.0, 69.0))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.address


class OrderItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='orders_item')
    drug = models.ForeignKey(Drug, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='orders_item')
