# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0042_auto_20161017_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='psicologo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
