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
            name='escolaridadeAvoMaterna',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='escolaridadeAvoMaterno',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='escolaridadeAvoPaterna',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='escolaridadeAvoPaterno',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='escolaridadeConjuge',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='escolaridadeMae',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='escolaridadePai',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='falecimentoAvoMaterna',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='falecimentoAvoMaterno',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='falecimentoAvoPaterna',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='falecimentoAvoPaterno',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='falecimentoMae',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='falecimentoPai',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoAvoMaterna',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoAvoMaterno',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoAvoPaterna',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoAvoPaterno',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoConjuge',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoMae',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nascimentoPai',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomeAvoMaterna',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomeAvoMaterno',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomeAvoPaterna',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomeAvoPaterno',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomeConjuge',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomeMae',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='nomePai',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='paciente',
            name='sexoConjuge',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
