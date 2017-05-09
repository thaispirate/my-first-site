# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0056_psicologo_bairro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chave',
            name='padrao',
            field=models.CharField(null=True, choices=[('usada', 'Usada'), ('livre', 'Livre')], max_length=20, blank=True),
        ),
    ]
