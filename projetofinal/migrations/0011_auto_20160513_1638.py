# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0010_auto_20160513_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaafetiva',
            name='afetivoRelacional',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='areaafetiva',
            name='espiritual',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='areaafetiva',
            name='organico',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='areaafetiva',
            name='produtividade',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='areaafetiva',
            name='socioCultural',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorA',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorB',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorC',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorD',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorE',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorF',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorG',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
