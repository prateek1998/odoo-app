from django.db import models

# Create your models here.
class Manual(models.Model):
    proxy_ip = models.TextField(default="10.210.210.117")
    port_no = models.TextField(default="2004")
    firmware = models.TextField(default="WC_16_10_0015.swi")
    tftp_server = models.TextField(default="10.101.101.79")