# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0058_paciente_habilitado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='habilitado',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
