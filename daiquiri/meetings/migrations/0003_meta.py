# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-23 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_meetings', '0002_meeting_registration_done_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='abstract',
            field=models.TextField(default='---', verbose_name='Abstract'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='contributions_message',
            field=models.TextField(blank=True, help_text='Message on contributions page, you can use Markdown here.', null=True, verbose_name='Contributions message'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='participants_message',
            field=models.TextField(blank=True, help_text='Message on participants page, you can use Markdown here.', null=True, verbose_name='Participants message'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='registration_done_message',
            field=models.TextField(blank=True, help_text='Message on the page displayed after registration, you can use Markdown here.', null=True, verbose_name='Registration done message'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='registration_message',
            field=models.TextField(blank=True, help_text='Message on registration page, you can use Markdown here.', null=True, verbose_name='Registration message'),
        ),
    ]
