# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0026_auto_20170223_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyfinancereportsumary',
            name='assetsPerShare',
            field=models.FloatField(default=0),
        ),
    ]
