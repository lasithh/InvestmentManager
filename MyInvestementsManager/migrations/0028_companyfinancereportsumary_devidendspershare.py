# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyInvestementsManager', '0027_companyfinancereportsumary_assetspershare'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyfinancereportsumary',
            name='devidendsPerShare',
            field=models.FloatField(default=0),
        ),
    ]
