# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0018_companyfinancereportsumary'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyfinancereportsumary',
            name='earning',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
