from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group


# Create your models here.


class Regions(models.Model):
    name_uz = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childs', on_delete=models.DO_NOTHING)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=150)

    def __str__(self):
        return self.name_uz


class Manufacturer(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class ReleaseForm(models.Model):
    name_uz = models.CharField(max_length=150)
    name_ru = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name_uz


class PharmGroup(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=150)
    description = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.name_uz


class InternationalName(models.Model):
    name_uz = models.CharField(max_length=225)
    name_ru = models.CharField(max_length=225)
    description = models.CharField(blank=True, null=True, max_length=1000)

    def __str__(self):
        return self.name_uz


class Drug(models.Model):
    region = models.ForeignKey(Regions, null=True, blank=True, on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.DO_NOTHING)
    release_form = models.ForeignKey(ReleaseForm, null=True, blank=True, on_delete=models.DO_NOTHING)
    pharm_group = models.ForeignKey(PharmGroup, blank=True, null=True, on_delete=models.DO_NOTHING)
    international_name = models.ForeignKey(InternationalName, blank=True, null=True, on_delete=models.DO_NOTHING)

    name_uz = models.CharField(max_length=150)
    name_ru = models.CharField(max_length=150, blank=True)
    price = models.CharField(max_length=120)
    image = models.ImageField(upload_to='static/drug_images')
    description_uz = RichTextField(blank=True, null=True)
    description_ru = RichTextField(blank=True, null=True)
    barcode = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.name_uz