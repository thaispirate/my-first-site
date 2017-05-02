# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0051_chave_padrao'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='tempo',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
