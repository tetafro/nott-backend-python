# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_auto_20151114_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='notepad',
            name='folder',
            field=models.ForeignKey(related_name='notepads', null=True, to='data.Folder'),
            preserve_default=False,
        ),
    ]
