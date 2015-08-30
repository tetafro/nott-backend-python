# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='notepad',
            name='title',
            field=models.CharField(max_length=32),
        ),
    ]
