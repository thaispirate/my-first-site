# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='nascimento',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nome',
            field=models.CharField(default=' ', max_length=50),
        ),
        migrations.AddField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(default=' ', max_length=1, choices=[('F', 'Feminino'), ('M', 'Masculino')]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='email',
            field=models.EmailField(default=' ', max_length=50),
        ),
    ]
