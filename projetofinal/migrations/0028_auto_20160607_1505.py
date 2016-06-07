# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0027_auto_20160606_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrauIndiferenciacao',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('padrao', models.CharField(choices=[('adaptativo', 'Adaptativo'), ('reativo', 'Reativo'), ('criativo', 'Criativo')], max_length=10, null=True)),
                ('resposta', models.TextField(null=True)),
                ('valor', models.FloatField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='relacionamento',
            name='parente',
            field=models.CharField(choices=[('Pai', 'Pai'), ('Mae', 'Mãe'), ('AvoPaterno', 'Avô Paterno'), ('AvoPaterna', 'Avó Paterna'), ('AvoMaterno', 'Avô Materno'), ('AvoMaterna', 'Avó Materna'), ('Paciente', 'Paciente'), ('Conjuge', 'Cônjuge')], max_length=10, null=True),
        ),
    ]
