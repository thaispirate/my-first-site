# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0002_auto_20160323_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='escolaridadeConjuge',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nascimentoConjuge',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nomeConjuge',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='sexoConjuge',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
    ]
