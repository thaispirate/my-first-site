# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0055_remove_psicologo_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='bairro',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
