# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='created',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='created',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='note',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='notepad',
            name='created',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='notepad',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
