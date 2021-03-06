# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListedCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=250)),
                ('symbol', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('issuedQuentity', models.BigIntegerField()),
                ('marketCapitalisation', models.BigIntegerField()),
                ('marketCapitalisationPercentage', models.FloatField()),
            ],
        ),
    ]
