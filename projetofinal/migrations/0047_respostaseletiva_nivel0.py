# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0046_auto_20161222_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel0',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
