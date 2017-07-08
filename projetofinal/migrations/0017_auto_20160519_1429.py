# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0016_auto_20160519_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anamnesia',
            name='fim',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='anamnesia',
            name='inicio',
            field=models.DateTimeField(null=True),
        ),
    ]
