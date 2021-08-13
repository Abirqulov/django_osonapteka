from ..models import Regions, Drug, Manufacturer, InternationalName, ReleaseForm, PharmGroup
from django.db.models import Q
from apps.stores.models import Remain
from rest_framework import serializers


class RegionListSerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Regions
        fields = ['name_uz', 'name_ru', 'slug', 'childs']

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('name_uz')
        return RegionListSerializer(childs, many=True).data


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name')


class ReleaseFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseForm
        fields = ('id', 'name_uz', 'name_ru')


class InternationalNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalName
        fields = ['id', 'name_uz', 'name_ru']


class PharmGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmGroup
        fields = ['id', 'name_uz', 'name_ru']


class RemainSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()

    class Meta:
        model = Remain
        fields = ('id', 'store', 'qty')

    def get_store(self, obj):
        return obj.store.name


class DrugListSerializer(serializers.ModelSerializer):
    region = RegionListSerializer(many=False, read_only=True)
    manufacture = ManufactureSerializer(many=False, read_only=True)
    international_name = InternationalNameSerializer(many=False, read_only=True)
    pharm_group = PharmGroupSerializer(many=False, read_only=True)
    release_form = ReleaseFormSerializer(many=False, read_only=True)
    remains = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Drug
        fields = ["id", 'manufacture', 'international_name', 'pharm_group', 'release_form',
                  'remains', 'image', 'price', 'name', 'description', 'barcode', 'slug']

    def get_name(self, drug):
        try:
            request = self.context.get('request')
            lan = request.GET('lan')
            name = drug.name_uz
            if lan == 'ru':
                if drug.name_ru:
                    name = drug.name_ru
            return name
        except:
            return drug.name

    def get_description(self, drug):
        request = self.context.get('request')
        lan = request.GET("lan", "ru")
        description = getattr(drug, 'description_' + lan)

        return description

    def get_remains(self, obj):
        request = self.context.get('request')
        if request.user.group.filter(name="manager").exists():
            remains = RemainSerializer(obj.remains.filter(qty__gt=0, store__status=True), many=True, read_only=True).data
            return remains
        else:
            return []