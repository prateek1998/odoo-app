# Generated by Django 3.2.5 on 2021-08-03 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manual',
            name='firmware',
            field=models.TextField(default='WC_16_10_0015.swi'),
        ),
        migrations.AlterField(
            model_name='manual',
            name='port_no',
            field=models.TextField(default='2004'),
        ),
        migrations.AlterField(
            model_name='manual',
            name='proxy_ip',
            field=models.TextField(default='10.210.210.117'),
        ),
        migrations.AlterField(
            model_name='manual',
            name='tftp_server',
            field=models.TextField(default='10.101.101.79'),
        ),
    ]