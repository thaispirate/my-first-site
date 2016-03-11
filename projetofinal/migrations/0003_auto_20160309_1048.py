# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0002_auto_20160309_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nome',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(null=True, choices=[('F', 'Feminino'), ('M', 'Masculino')], max_length=1),
        ),
    ]
