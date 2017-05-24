# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0059_auto_20170510_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('estado', models.CharField(null=True, blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('municipio', models.CharField(null=True, blank=True, max_length=100)),
                ('estado', models.ForeignKey(null=True, to='projetofinal.Estado')),
            ],
        ),
    ]
