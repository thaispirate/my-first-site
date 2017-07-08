# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0007_auto_20160510_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorA',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorB',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorC',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorD',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorE',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorF',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionarioareaafetiva',
            name='valorG',
            field=models.TextField(blank=True, null=True),
        ),
    ]
