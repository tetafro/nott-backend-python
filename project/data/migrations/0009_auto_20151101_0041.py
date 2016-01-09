# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20151101_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergeo',
            name='city',
            field=models.CharField(max_length=16, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='country_code',
            field=models.CharField(max_length=2, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='country_name',
            field=models.CharField(max_length=16, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='ip',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='metro_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='region_code',
            field=models.CharField(max_length=8, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='region_name',
            field=models.CharField(max_length=32, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='time_zone',
            field=models.CharField(max_length=16, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usergeo',
            name='zip_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
