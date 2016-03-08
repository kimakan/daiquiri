# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 16:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField()),
                ('label', models.CharField(max_length=256)),
                ('data_type', models.CharField(choices=[('text', 'Text'), ('textarea', 'Textarea'), ('checkbox', 'Checkbox'), ('radio', 'Radio button'), ('select', 'Select'), ('multiselect', 'Multiselect')], max_length=11)),
                ('help_text', models.TextField(blank=True, help_text='Enter a help text to be displayed next to the input element')),
                ('options', jsonfield.fields.JSONField(blank=True, help_text='Enter valid JSON of the form [[key, label], [key, label], ...]', null=True)),
                ('required', models.BooleanField()),
            ],
            options={
                'ordering': ('key',),
                'verbose_name': 'DetailKey',
                'verbose_name_plural': 'DetailKeys',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', jsonfield.fields.JSONField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user',),
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
