# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0070_auto_20170805_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='psicologo',
            name='celular',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='psicologo',
            name='telefone',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
