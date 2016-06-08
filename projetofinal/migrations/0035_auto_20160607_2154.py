# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0034_auto_20160607_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respostaseletiva',
            name='pergunta',
            field=models.ForeignKey(to='projetofinal.PerguntaSeletiva', null=True),
        ),
    ]
