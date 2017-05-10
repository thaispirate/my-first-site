# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0057_auto_20170509_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='habilitado',
            field=models.DateField(null=True),
        ),
    ]
