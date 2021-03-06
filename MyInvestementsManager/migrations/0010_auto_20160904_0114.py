# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 23:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0009_auto_20160903_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectorIndexNames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='sectorindex',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyInvestementsManager.SectorIndexNames'),
        ),
    ]
