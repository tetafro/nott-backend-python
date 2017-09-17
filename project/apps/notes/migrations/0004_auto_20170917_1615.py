# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20170911_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notes'),
        ),
        migrations.AlterField(
            model_name='notepad',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notepad',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='notepads'),
        ),
    ]
