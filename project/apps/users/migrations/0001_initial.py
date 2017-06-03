# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.users.models
import django.utils.timezone
import apps.users.helpers


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=40)),
                ('email', models.CharField(unique=True, max_length=40)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('avatar', models.FileField(blank=True, null=True, storage=apps.users.helpers.OverwriteStorage(), upload_to=apps.users.models.User._upload_to)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
