# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0071_auto_20170814_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(max_length=14, null=True),
        ),
    ]
