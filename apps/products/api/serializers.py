from ..models import Regions, Drug, Manufacturer, InternationalName, ReleaseForm
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
        fields = ('id', 'name_uz', 'name_ru')


class ReleaseFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseForm
        fields = ('id', 'name_uz', 'name_ru')





class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('__all__')