# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0038_redomendacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recomendacao',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('nome', models.CharField(max_length=20, null=True)),
                ('intervalo', models.CharField(max_length=10, null=True, choices=[('minimo', 'Mínimo'), ('medio', 'Médio'), ('maximo', 'Máximo')])),
                ('texto', models.TextField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Redomendacao',
        ),
    ]
