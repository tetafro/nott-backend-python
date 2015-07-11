# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Notepad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32)),
                ('user', models.ForeignKey(related_name='notepads', to='main.User')),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='notepad',
            field=models.ForeignKey(related_name='notes', to='main.Notepad'),
        ),
    ]
