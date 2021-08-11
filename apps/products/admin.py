from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Regions)
admin.site.register(Manufacturer)
admin.site.register(ReleaseForm)
admin.site.register(PharmGroup)
admin.site.register(InternationalName)
admin.site.register(Drug)