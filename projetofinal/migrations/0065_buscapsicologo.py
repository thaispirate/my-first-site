# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0064_auto_20170516_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuscaPsicologo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('estado', models.ForeignKey(null=True, to='projetofinal.Estado')),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(null=True, auto_choose=True, to='projetofinal.Municipio', chained_model_field='estado', chained_field='estado')),
            ],
        ),
    ]
