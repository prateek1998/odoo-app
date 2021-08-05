from django.db import models
import datetime

# Create your models here.
class Manual(models.Model):
    proxy_ip = models.TextField(default="10.210.210.117")
    port_no = models.TextField(default="2004")
    firmware = models.TextField(default="WC_16_10_0015.swi")
    tftp_server = models.TextField(default="10.101.101.79")

class Firmware_Records(models.Model):
    switch_vendor = models.CharField(max_length=64, blank=True, null=True)
    time = models.DateTimeField(default=datetime.datetime.now)
    old_firmware = models.CharField(max_length=64, blank=True, null=True)
    mac_address = models.CharField(max_length=64, blank=True, null=True)
    new_firmware = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True)
    
