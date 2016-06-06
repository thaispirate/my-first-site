# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0023_auto_20160603_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relacionamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('parente', models.CharField(max_length=10, null=True)),
                ('relacao', models.CharField(max_length=20, null=True)),
                ('filhos', models.IntegerField(null=True, blank=True)),
                ('filhas', models.IntegerField(null=True, blank=True)),
                ('relacaoAntes', models.CharField(max_length=20, null=True)),
                ('filhosAntes', models.IntegerField(null=True, blank=True)),
                ('filhasAntes', models.IntegerField(null=True, blank=True)),
                ('filhosDepois', models.IntegerField(null=True, blank=True)),
                ('filhasDepois', models.IntegerField(null=True, blank=True)),
                ('paciente', models.ForeignKey(to='projetofinal.Paciente', null=True)),
            ],
        ),
    ]
