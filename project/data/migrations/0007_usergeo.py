# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0006_auto_20151010_2357'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGeo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(related_name='geo_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
