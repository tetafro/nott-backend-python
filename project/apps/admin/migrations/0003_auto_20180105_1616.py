# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_auto_20171204_0812'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Config',
            new_name='Setting',
        ),
    ]
