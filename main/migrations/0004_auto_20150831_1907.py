# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150828_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='notepad',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
