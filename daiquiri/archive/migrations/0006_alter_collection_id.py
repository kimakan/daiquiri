# Generated by Django 3.2.10 on 2021-12-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_archive', '0005_django2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
