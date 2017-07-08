# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0031_grauindiferenciacaopaciente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anamnesia',
            name='GrauDiferenciacao',
        ),
        migrations.AddField(
            model_name='anamnesia',
            name='padrao',
            field=models.CharField(choices=[('adaptativo', 'Adaptativo'), ('reativo', 'Reativo'), ('criativo', 'Criativo')], max_length=20, null=True, blank=True),
        ),
    ]
