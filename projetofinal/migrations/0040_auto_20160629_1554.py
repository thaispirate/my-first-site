# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0039_auto_20160629_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recomendacao',
            name='intervalo',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
