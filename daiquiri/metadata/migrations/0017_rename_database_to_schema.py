# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-16 17:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_metadata', '0016_rename_database_to_schema'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Database',
            new_name='Schema',
        ),
        migrations.AlterModelOptions(
            name='schema',
            options={'ordering': ('order',), 'permissions': (('view_schema', 'Can view Schema'),), 'verbose_name': 'Schema', 'verbose_name_plural': 'Schemas'},
        ),
    ]
