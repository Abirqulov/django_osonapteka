from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=125)
    image = models.ImageField(upload_to='static/images')
    description = models.TextField()
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='childs', on_delete=models.DO_NOTHING)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=125)

    def __str__(self):
        return self.name


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


class DrugObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()


class DrugManager(models.Manager):
    def get_queryset(self, region=(1,)):

        query = super().get_queryset()\
            .annotate(remain_sum=models.Sum("remains__qty",
                                            filter=models.Q(remains__store__status=True,
                                                            remains__store__region_id__in=region)))\
            .annotate(price=models.Min("remains__price", filter=(models.Q(remains__price__gt=50) &
                                                                 models.Q(remains__store__status=True) &
                                                                 models.Q(remains__qty__gt=0) &
                                                                 models.Q(remains__store__region_id__in=region))))\
            .filter(status=True, price__gt=50)

        return query

    def for_region(self, region):
        return self.get_queryset(region=(region,))

    def for_region_in(self, region_ids):
        return self.get_queryset(region=region_ids)


class Drug(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.DO_NOTHING)
    release_form = models.ForeignKey(ReleaseForm, null=True, blank=True, on_delete=models.DO_NOTHING)
    pharm_group = models.ForeignKey(PharmGroup, blank=True, null=True, on_delete=models.DO_NOTHING)
    international_name = models.ForeignKey(InternationalName, blank=True, null=True, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='static/drug_images')
    description_uz = RichTextField(blank=True, null=True)
    description_ru = RichTextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    barcode = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(max_length=120, null=True, blank=True)

    objects = DrugObjectsManager()
    products = DrugManager()

    def __str__(self):
        return self.name_uz