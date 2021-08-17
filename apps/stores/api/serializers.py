from ..models import Store, Remain, Regions
from rest_framework import serializers


class RegionListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    childs = serializers.SerializerMethodField(read_only=True)
    coords = serializers.SerializerMethodField()

    class Meta:
        model = Regions
        fields = ('id', 'name', 'childs', 'coords')

    def get_name(self, obj):
        request = self.context.get('request')
        data = request.GET if hasattr(request, 'GET') else {}
        language = data['lan'] if 'lan' in data else 'uz'
        return getattr(obj, 'name_' + language)

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('name_uz')
        return RegionListSerializer(childs, many=True).data

    def get_coords(self, obj):
        return obj.polygon.centroid.coords


class StoreSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField(read_only=True)
    orders_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Store
        fields = ["id", "name", "image", "address", "phone", "location", "distance", "orders_count"]

    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance, 1)
        else:
            return None

    def get_orders_count(self, obj):
        if hasattr(obj, 'orders_count'):
            return round(obj.orders_count, 1)
        else:
            return None