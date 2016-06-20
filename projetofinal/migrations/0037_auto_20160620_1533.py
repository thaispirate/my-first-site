# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0036_auto_20160608_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='perguntaseletiva',
            name='tipo',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='tipo',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='familia',
            name='nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='familia',
            name='nome',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='escolaridade',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
    ]
