# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0014_remove_areaafetiva_pergunta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anamnesia',
            name='areaAfetiva',
            field=models.ForeignKey(to='projetofinal.AreaAfetiva', null=True),
        ),
        migrations.AlterField(
            model_name='respostaareaafetiva',
            name='resposta',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='respostaareaafetiva',
            name='valor',
            field=models.FloatField(null=True),
        ),
    ]
