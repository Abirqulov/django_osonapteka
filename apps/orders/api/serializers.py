from apps.products.models import *
from ..models import *
from rest_framework import serializers
from apps.products.api.serializers import ManufacturerSerializer
from apps.stores.api.serializers import StoreSerializer
from apps.stores.models import *


class DrugSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(many=False)

    class Meta:
        model = Drug
        fields = ('id', 'name_uz', 'name_ru', 'image', 'manufacturer', 'barcode')


class OrderItemSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(many=False, read_only=True)
    store = StoreSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'drug', 'qty', 'price', 'subtotal', 'status', 'store']


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'phone', 'address', 'created_at', 'items']