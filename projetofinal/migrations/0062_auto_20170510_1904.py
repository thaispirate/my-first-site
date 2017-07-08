# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0061_estado_sigla'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='psicologo',
            name='cidade',
        ),
        migrations.AddField(
            model_name='psicologo',
            name='municipio',
            field=models.ForeignKey(to='projetofinal.Municipio', null=True),
        ),
        migrations.AlterField(
            model_name='psicologo',
            name='estado',
            field=models.ForeignKey(to='projetofinal.Estado', null=True),
        ),
    ]
