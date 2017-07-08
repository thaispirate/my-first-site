# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0067_auto_20170518_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='celular',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
