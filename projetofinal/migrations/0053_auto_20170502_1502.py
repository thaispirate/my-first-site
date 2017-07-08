# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0052_paciente_tempo'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='cidade',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='psicologo',
            name='codigo',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='psicologo',
            name='estado',
            field=models.CharField(null=True, max_length=50),
        ),
    ]
