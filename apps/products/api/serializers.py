from ..models import Drug, Manufacturer, InternationalName, ReleaseForm, PharmGroup, Category
from django.db.models import Q
from apps.stores.models import Remain, Region
from rest_framework import serializers


class CategoryListSerializers(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'childs', 'image', 'slug']

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('name')
        return CategoryListSerializers(childs, many=True).data


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name')


class ReleaseFormSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ReleaseForm
        fields = ('id', 'name')

    def get_name(self, release_form):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan')
            name = release_form.name_uz
            if lan == 'ru':
                name = release_form.name_ru
                return name
            elif lan == 'uz':
                name = release_form.name_uz
                return name
            else:
                return name
        except:
            return release_form.name_uz


class InternationalNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = InternationalName
        fields = ['id', 'name']

    def get_name(self, international_name):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan')
            name = international_name.name_uz
            if lan == 'ru':
                name = international_name.name_ru
                return name
            elif lan == 'uz':
                name = international_name.name_uz
                return name
            else:
                return name
        except:
            return international_name.name_uz


class PharmGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = PharmGroup
        fields = ['id', 'name']

    def get_name(self, pharm_group):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan')
            name = pharm_group.name_uz
            if lan == 'ru':
                name = pharm_group.name_ru
                return name
            elif lan == 'uz':
                name = pharm_group.name_uz
                return name
            else:
                return name
        except:
            return pharm_group.name_uz


class RemainSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()

    class Meta:
        model = Remain
        fields = ('id', 'store', 'qty')

    def get_store(self, obj):
        return obj.store.name


class DrugSerializer(serializers.ModelSerializer):
    category = CategorySerializers(many=True, read_only=True)
    manufacture = ManufacturerSerializer(many=False, read_only=True)
    international_name = InternationalNameSerializer(many=False, read_only=True)
    pharm_group = PharmGroupSerializer(many=False, read_only=True)
    release_form = ReleaseFormSerializer(many=False, read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    remains = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Drug
        fields = ["id", 'manufacture', 'international_name', 'pharm_group', 'release_form',
                  'remains', 'image', 'price', 'name', 'description', 'barcode', 'slug', 'category', 'status']

    def get_remains(self, obj):
        request = self.context.get('request')
        if request.user.groups.filter(name='manager').exists():
            return RemainSerializer(obj.remains.filter(qty__gt=0), many=True, read_only=True).data
        else:
            return []

    def get_name(self, drug):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan')
            name = drug.name_uz
            if lan == 'ru':
                name = drug.name_ru
                return name
            elif lan == 'uz':
                name = drug.name_uz
                return name
            else:
                return name
        except:
            return drug.name_uz

    def get_description(self, obj):
        request = self.context.get('request')
        lan = request.GET.get("lan")
        description = obj.description_uz
        if lan == "uz":
            description = obj.description_uz
            return description
        elif lan == "ru":
            description = obj.description_ru
            return description
        else:
            return description

    def get_price(self, obj):
        if hasattr(obj, 'price') and obj.price is not None:
            return obj.price
        else:
            return 0.0

class DrugListSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(many=False, read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Drug
    fields = ['id', 'name', 'slug', 'barcode', 'image', 'remains', 'price']

    def get_remains(self, obj):
        request = self.context.get('request')
        if request.user.groups.filter(name='manager').exists():
            return RemainSerializer(obj.remains.filter(qty__gt=0), many=True, read_only=True).data
        else:
            return []

    def get_price(self, obj):
        if hasattr(obj, 'price'):
            return obj.price
        else:
            return 0.0