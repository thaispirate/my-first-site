# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0013_areaafetiva_pergunta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areaafetiva',
            name='pergunta',
        ),
    ]
