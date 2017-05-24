# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0062_auto_20170510_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='complemento',
            field=models.CharField(null=True, max_length=200),
        ),
        migrations.AddField(
            model_name='psicologo',
            name='endereco',
            field=models.CharField(null=True, max_length=200),
        ),
        migrations.AddField(
            model_name='psicologo',
            name='numero',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='psicologo',
            name='telefone',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='psicologo',
            name='municipio',
            field=smart_selects.db_fields.ChainedForeignKey(null=True, chained_field='continent', to='projetofinal.Municipio', chained_model_field='continent', auto_choose=True),
        ),
    ]
