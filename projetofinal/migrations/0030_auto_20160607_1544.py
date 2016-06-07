# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0029_auto_20160607_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grauindiferenciacao',
            name='valor',
        ),
        migrations.AlterField(
            model_name='anamnesia',
            name='retornos',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhas',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhasAntes',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhasDepois',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhos',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhosAntes',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='filhosDepois',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
