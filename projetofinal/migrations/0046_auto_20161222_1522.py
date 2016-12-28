# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0045_auto_20161130_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='respostainterventiva',
            name='nivel6',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel6',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
