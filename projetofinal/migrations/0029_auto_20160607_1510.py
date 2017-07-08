# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0028_auto_20160607_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grauindiferenciacao',
            name='valor',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
