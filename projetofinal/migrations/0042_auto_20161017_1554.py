# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0041_auto_20161017_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='respostainterventiva',
            name='nivel1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostainterventiva',
            name='nivel2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostainterventiva',
            name='nivel3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostainterventiva',
            name='nivel4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostainterventiva',
            name='nivel5',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel3',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel4',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='respostaseletiva',
            name='nivel5',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
