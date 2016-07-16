# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.users.models
import apps.users.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, upload_to=apps.users.models.User.upload_to, null=True, storage=apps.users.helpers.OverwriteStorage()),
        ),
    ]
