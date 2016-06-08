# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0032_auto_20160607_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerguntaSeletiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespostaSeletiva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letra', models.CharField(max_length=1, null=True)),
                ('resposta', models.TextField(null=True)),
                ('valor', models.FloatField(null=True)),
                ('pergunta', models.ForeignKey(to='projetofinal.PerguntaAreaAfetiva', null=True)),
            ],
        ),
    ]
