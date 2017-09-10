# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_auto_20170903_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='notes'),
        ),
        migrations.AddField(
            model_name='notepad',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='notepads'),
        ),
    ]
