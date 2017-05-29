# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.users.models
import apps.users.helpers
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(unique=True, max_length=40)),
                ('email', models.CharField(unique=True, max_length=40)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(null=True, auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('avatar', models.FileField(upload_to=apps.users.models.User._upload_to, blank=True, null=True, storage=apps.users.helpers.OverwriteStorage())),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserGeo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('ip', models.CharField(blank=True, null=True, max_length=15)),
                ('country_code', models.CharField(blank=True, null=True, max_length=2)),
                ('country_name', models.CharField(blank=True, null=True, max_length=16)),
                ('region_code', models.CharField(blank=True, null=True, max_length=8)),
                ('region_name', models.CharField(blank=True, null=True, max_length=32)),
                ('city', models.CharField(blank=True, null=True, max_length=16)),
                ('zip_code', models.CharField(blank=True, null=True, max_length=8)),
                ('time_zone', models.CharField(blank=True, null=True, max_length=16)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('metro_code', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(related_name='geo_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
