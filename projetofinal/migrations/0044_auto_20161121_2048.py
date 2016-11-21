# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0043_paciente_psicologo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='psicologo',
            field=models.ForeignKey(null=True, to='projetofinal.Psicologo'),
        ),
    ]
