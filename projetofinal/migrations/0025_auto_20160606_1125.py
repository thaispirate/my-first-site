# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0024_relacionamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='parente',
            field=models.CharField(null=True, choices=[('pai', 'Pai'), ('mae', 'Mãe'), ('avoPaterno', 'Avô Paterno'), ('avoPaterna', 'Avó Paterna'), ('avoMaterno', 'Avô Materno'), ('avoMaterna', 'Avó Materna'), ('conjuge', 'Cônjuge')], max_length=10),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhas',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='parente',
            field=models.CharField(null=True, choices=[('pai', 'Pai'), ('mae', 'Mãe'), ('avoPaterno', 'Avô Paterno'), ('avoPaterna', 'Avó Paterna'), ('avoMaterno', 'Avô Materno'), ('avoMaterna', 'Avó Materna'), ('conjuge', 'Cônjuge')], max_length=10),
        ),
    ]
