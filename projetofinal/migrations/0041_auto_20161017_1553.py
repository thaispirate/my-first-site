# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0040_auto_20160629_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='respostaareaafetiva',
            name='nivel1',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='respostaareaafetiva',
            name='nivel2',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='respostaareaafetiva',
            name='nivel3',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='respostaareaafetiva',
            name='nivel4',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='respostaareaafetiva',
            name='nivel5',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nascimento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
