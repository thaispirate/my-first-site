# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0022_auto_20160603_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familia',
            name='usuario',
            field=models.ForeignKey(to='projetofinal.Paciente', null=True),
        ),
    ]
