# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0065_buscapsicologo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='psicologo',
            old_name='codigo',
            new_name='crp',
        ),
    ]
