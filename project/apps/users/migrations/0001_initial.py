# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import apps.users.helpers
import django.utils.timezone
import apps.users.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('avatar', models.FileField(upload_to=apps.users.models.User._upload_to, null=True, storage=apps.users.helpers.OverwriteStorage(), blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserGeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=15, null=True, blank=True)),
                ('country_code', models.CharField(max_length=2, null=True, blank=True)),
                ('country_name', models.CharField(max_length=16, null=True, blank=True)),
                ('region_code', models.CharField(max_length=8, null=True, blank=True)),
                ('region_name', models.CharField(max_length=32, null=True, blank=True)),
                ('city', models.CharField(max_length=16, null=True, blank=True)),
                ('zip_code', models.IntegerField(null=True, blank=True)),
                ('time_zone', models.CharField(max_length=16, null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('metro_code', models.IntegerField(null=True, blank=True)),
                ('user', models.OneToOneField(related_name='geo_info', to=settings.AUTH_USER_MODEL)),
            ],
        )
    ]
