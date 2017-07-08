# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0025_auto_20160606_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='relacionamento',
            name='anamnesia',
            field=models.ForeignKey(to='projetofinal.Anamnesia', null=True),
        ),
    ]
