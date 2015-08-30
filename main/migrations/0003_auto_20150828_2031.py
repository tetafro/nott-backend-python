# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150827_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='notepad',
            name='parent',
            field=models.ForeignKey(to='main.Notepad', default=1, related_name='children'),
        ),
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
