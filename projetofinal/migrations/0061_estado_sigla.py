# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0060_estado_municipio'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='sigla',
            field=models.CharField(null=True, blank=True, max_length=3),
        ),
    ]
