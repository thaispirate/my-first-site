# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0009_auto_20160513_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areaafetiva',
            name='area',
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='afetivoRelacional',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='espiritual',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='organico',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='paciente',
            field=models.ForeignKey(to='projetofinal.Paciente', null=True),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='produtividade',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='socioCultural',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='anamnesia',
            name='area',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='anamnesia',
            name='fim',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='anamnesia',
            name='paciente',
            field=models.ForeignKey(to='projetofinal.Paciente', null=True),
        ),
    ]
