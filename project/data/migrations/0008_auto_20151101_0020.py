# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_usergeo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergeo',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='geo_info'),
        ),
    ]
