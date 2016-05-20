# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0017_auto_20160519_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaafetiva',
            name='anamnesia',
            field=models.ForeignKey(null=True, to='projetofinal.Anamnesia'),
        ),
    ]
