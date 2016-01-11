# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.data.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20151006_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notepad',
            name='parent',
            field=models.ForeignKey(to='apps.data.Notepad', null=True, related_name='children'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FileField(upload_to=apps.data.helpers.avatar_filename, storage=apps.data.helpers.OverwriteStorage(), blank=True, null=True),
        ),
    ]
