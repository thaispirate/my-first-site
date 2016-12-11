# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0044_auto_20161121_2048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='familia',
            old_name='usuario',
            new_name='paciente',
        ),
    ]
