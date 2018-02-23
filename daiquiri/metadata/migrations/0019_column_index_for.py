# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-23 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_metadata', '0018_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='index_for',
            field=models.CharField(blank=True, help_text='The columns which this column is an index for (e.g. for pgSphere).', max_length=256, null=True, verbose_name='Index for'),
        ),
    ]
