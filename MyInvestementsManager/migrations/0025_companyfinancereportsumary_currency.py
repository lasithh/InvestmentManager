# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0024_dividends_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyfinancereportsumary',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='MyInvestementsManager.Currency'),
        ),
    ]
