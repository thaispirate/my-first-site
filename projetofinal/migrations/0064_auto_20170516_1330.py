# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0063_auto_20170516_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psicologo',
            name='municipio',
            field=smart_selects.db_fields.ChainedForeignKey(to='projetofinal.Municipio', null=True, chained_model_field='estado', auto_choose=True, chained_field='estado'),
        ),
    ]
