# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0015_auto_20160519_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anamnesia',
            name='areaAfetiva',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
