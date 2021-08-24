from ..models import Store, Remain, Region
from rest_framework import serializers
from django.db.models import Q, Sum, Min


class RegionListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    childs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Region
        fields = ('id', 'name', 'childs')

    def get_name(self, obj):
        request = self.context.get('request')
        lan = request.GET.get("lan")
        name = obj.name_uz
        if lan == "ru":
            name = obj.name_ru
            return name
        elif lan == "uz":
            name = obj.name_uz
            return name
        else:
            return name

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('name_uz')
        request = self.context.get('request')
        return RegionListSerializer(childs, many=True, context={'request': request}).data


class RemainSerializer(serializers.ModelSerializer):
    drug_id = serializers.IntegerField(source='drug_id', read_only=True)
    drug_name = serializers.CharField(source='drug_full_name', read_only=True)
    qty = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Remain
        fields = ['id', 'store', 'drug_name', 'name', 'drug_id', 'qty', 'price']

    def get_qty(self, obj):
        request = self.context.get('request')
        if 'products' in request.data:
            products = request.data['products']
        else:
            return []
        for item in products:
            if item.get('drug_id') == obj.grud.id:
                return item.get('qty', 1)
        return 1


class StoreSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField(read_only=True)
    remains = serializers.SerializerMethodField(read_only=True)
    updated_at = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'price', 'remains', 'updated_at', 'address', 'location', 'image', 'phone']

    def get_name(self, obj):
        request = self.context.get('request')
        lan = request.GET.get("lan")
        name = obj.name_uz
        if lan == "uz":
            name = obj.name_uz
            return name
        elif lan == "ru":
            name = obj.name_ru
            return name
        else:
            return name

    def get_address(self, obj):
        request = self.context.get('request')
        lan = request.GET.get("lan")
        address = obj.address_uz
        if lan == "uz":
            address = obj.address_uz
            return address
        elif lan == 'ru':
            address = obj.addres_ru
            return address
        else:
            return address

    def get_price(self, obj):
        if hasattr(obj, 'price'):
            return obj.price
        else:
            return 0.0

    def get_remains(self, obj):
        request = self.context.get('request')
        if 'products' in request.data:
            products = request.data['products']
        else:
            return []
        remains = obj.remains
        query = Q()
        items = {}
        for item in products:
            items[item['drug_id']] = item.get("qty", 1)
            subquery = Q(qty__gt=0) & Q(drug_id=item['drug_id'])
            query |= subquery
        remains = remains.filter(query, publish=True)
        remains = remains.order_by('drug_id', 'price')
        remains = remains.distinct('drug_id')
        return RemainSerializer(remains, many=True, context={'request': request}).data