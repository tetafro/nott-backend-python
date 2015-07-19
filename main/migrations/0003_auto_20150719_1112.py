# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150711_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
