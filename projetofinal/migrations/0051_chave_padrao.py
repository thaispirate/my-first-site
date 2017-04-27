# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0050_paciente_retornos'),
    ]

    operations = [
        migrations.AddField(
            model_name='chave',
            name='padrao',
            field=models.CharField(max_length=20, blank=True, null=True, choices=[('usada', 'Usada')]),
        ),
    ]
