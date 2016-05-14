# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0008_auto_20160513_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorA',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorB',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorC',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorD',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorE',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorF',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='valorG',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
