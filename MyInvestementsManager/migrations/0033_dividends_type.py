# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-10 00:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0032_auto_20180909_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='dividends',
            name='type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='MyInvestementsManager.DividendTypes'),
            preserve_default=False,
        ),
    ]
