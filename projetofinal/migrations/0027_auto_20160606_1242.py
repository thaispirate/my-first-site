# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0026_relacionamento_anamnesia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacionamento',
            name='parente',
            field=models.CharField(choices=[('pai', 'Pai'), ('mae', 'Mãe'), ('avoPaterno', 'Avô Paterno'), ('avoPaterna', 'Avó Paterna'), ('avoMaterno', 'Avô Materno'), ('avoMaterna', 'Avó Materna'), ('paciente', 'Paciente'), ('conjuge', 'Cônjuge')], max_length=10, null=True),
        ),
    ]
