from ..models import Regions, Drug, Manufacturer, InternationalName, ReleaseForm, PharmGroup
from django.db.models import Q
from apps.stores.models import Remain
from rest_framework import serializers


def get_language(request):
    lan = request.GET.get('lan')
    if lan is None:
        lan = 'uz'
    return lan


class RegionListSerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Regions
        fields = ['name', 'slug', 'childs']

    def get_childs(self, instance):
        childs = instance.childs.all().order_by('name_uz')
        request = self.context.get('request')
        return RegionListSerializer(childs, many=True, context={'request': request}).data

    def get_name(self, region_name):
        try:
            request = self.context.get('request')
            lan = request.GET.get('lan', 'uz')
            name = region_name.name_uz
            if lan == 'ru':
                name = region_name.name_ru
                return name
            elif lan == 'uz':
                name = region_name.name_uz
                return name
            else:
                return name
        except:
            return region_name.name_uz


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


class DrugListSerializer(serializers.ModelSerializer):
    region = RegionListSerializer(many=False, read_only=True)
    manufacture = ManufacturerSerializer(many=False, read_only=True)
    international_name = InternationalNameSerializer(many=False, read_only=True)
    pharm_group = PharmGroupSerializer(many=False, read_only=True)
    release_form = ReleaseFormSerializer(many=False, read_only=True)
    remains = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Drug
        fields = ["id", 'manufacture', 'international_name', 'pharm_group', 'release_form',
                  'remains', 'image', 'price', 'name', 'description', 'barcode', 'slug', 'region']

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

    def get_description(self, drug):
        request = self.context.get('request')
        lan = request.GET.get("lan", "ru")
        description = getattr(drug, 'description_' + lan)

        return description

    def get_remains(self, obj):
        request = self.context.get('request')
        if request.user.groups.filter(name="manager").exists():
            remains = RemainSerializer(obj.remains.filter(qty__gt=0, store__status=True), many=True, read_only=True).data
            return remains
        else:
            return []


