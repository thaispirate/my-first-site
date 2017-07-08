# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0053_auto_20170502_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
