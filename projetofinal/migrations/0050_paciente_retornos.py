# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0049_auto_20170410_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='retornos',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
