# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20151010_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notepad',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, related_name='children', to='data.Notepad'),
        ),
    ]
