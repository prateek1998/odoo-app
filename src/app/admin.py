from django.contrib import admin
from .models import Manual
from .models import Firmware_Records
# Register your models here.
admin.site.register(Manual)
admin.site.register(Firmware_Records)