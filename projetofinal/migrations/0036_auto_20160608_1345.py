# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0035_auto_20160607_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interventiva',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('anamnesia', models.ForeignKey(null=True, to='projetofinal.Anamnesia')),
                ('paciente', models.ForeignKey(null=True, to='projetofinal.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='PerguntaInterventiva',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespostaInterventiva',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('letra', models.CharField(max_length=1, null=True)),
                ('resposta', models.TextField(null=True)),
                ('pergunta', models.ForeignKey(null=True, to='projetofinal.PerguntaInterventiva')),
            ],
        ),
        migrations.AddField(
            model_name='interventiva',
            name='resposta',
            field=models.ForeignKey(null=True, to='projetofinal.RespostaInterventiva'),
        ),
    ]
