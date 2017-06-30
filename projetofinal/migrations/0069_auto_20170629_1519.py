# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0068_psicologo_celular'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='paciente',
            name='telefone',
            field=models.CharField(null=True, max_length=50),
        ),
    ]
