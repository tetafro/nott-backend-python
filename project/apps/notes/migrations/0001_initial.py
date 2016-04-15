# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('parent', models.ForeignKey(null=True, to='notes.Folder', blank=True, related_name='subfolders')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='folders')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notepad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('folder', models.ForeignKey(null=True, to='notes.Folder', related_name='notepads')),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='notepad',
            field=models.ForeignKey(to='notes.Notepad', related_name='notes'),
        ),
    ]
