# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0037_auto_20160620_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redomendacao',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('intervalo', models.CharField(max_length=10, null=True, choices=[('minimo', 'Mínimo'), ('medio', 'Médio'), ('maximo', 'Máximo')])),
                ('texto', models.TextField(null=True)),
                ('nome', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
