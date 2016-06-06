# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0020_delete_monthlyweatherbycity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Famlia',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('parente', models.CharField(null=True, max_length=10)),
                ('nome', models.CharField(null=True, max_length=50)),
                ('nascimento', models.DateField(null=True)),
                ('falecimento', models.DateField(null=True, blank=True)),
                ('sexo', models.CharField(null=True, blank=True, max_length=10)),
                ('escolaridade', models.CharField(null=True, blank=True, max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadeAvoMaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadeAvoMaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadeAvoPaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadeAvoPaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadeConjuge',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadeMae',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='escolaridadePai',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='falecimentoAvoMaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='falecimentoAvoMaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='falecimentoAvoPaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='falecimentoAvoPaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='falecimentoMae',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='falecimentoPai',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoAvoMaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoAvoMaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoAvoPaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoAvoPaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoConjuge',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoMae',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nascimentoPai',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomeAvoMaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomeAvoMaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomeAvoPaterna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomeAvoPaterno',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomeConjuge',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomeMae',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nomePai',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='sexoConjuge',
        ),
        migrations.AddField(
            model_name='famlia',
            name='usuario',
            field=models.OneToOneField(to='projetofinal.Paciente'),
        ),
    ]
