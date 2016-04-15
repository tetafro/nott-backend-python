# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import apps.users.helpers


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('avatar', models.FileField(upload_to=apps.users.helpers.avatar_filename, blank=True, null=True, storage=apps.users.helpers.OverwriteStorage())),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserGeo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, blank=True, null=True)),
                ('country_code', models.CharField(max_length=2, blank=True, null=True)),
                ('country_name', models.CharField(max_length=16, blank=True, null=True)),
                ('region_code', models.CharField(max_length=8, blank=True, null=True)),
                ('region_name', models.CharField(max_length=32, blank=True, null=True)),
                ('city', models.CharField(max_length=16, blank=True, null=True)),
                ('zip_code', models.IntegerField(blank=True, null=True)),
                ('time_zone', models.CharField(max_length=16, blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('metro_code', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(related_name='geo_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
