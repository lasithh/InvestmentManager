# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-19 06:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0041_auto_20190609_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('tables', models.BinaryField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyInvestementsManager.ListedCompany')),
            ],
        ),
    ]
