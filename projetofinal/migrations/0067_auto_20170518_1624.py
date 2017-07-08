# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0066_auto_20170516_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buscapsicologo',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='buscapsicologo',
            name='municipio',
        ),
        migrations.DeleteModel(
            name='BuscaPsicologo',
        ),
    ]
