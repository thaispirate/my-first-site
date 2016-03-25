# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0003_auto_20160323_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='falecimentoAvoMaterna',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='falecimentoAvoMaterno',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='falecimentoAvoPaterna',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='falecimentoAvoPaterno',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='falecimentoMae',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='falecimentoPai',
            field=models.DateField(null=True, blank=True),
        ),
    ]
