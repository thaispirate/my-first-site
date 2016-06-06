# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0021_auto_20160603_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('parente', models.CharField(max_length=10, null=True)),
                ('nome', models.CharField(max_length=50, null=True)),
                ('nascimento', models.DateField(null=True)),
                ('falecimento', models.DateField(null=True, blank=True)),
                ('sexo', models.CharField(max_length=10, null=True, blank=True)),
                ('escolaridade', models.CharField(max_length=15, null=True, blank=True)),
                ('usuario', models.OneToOneField(to='projetofinal.Paciente')),
            ],
        ),
        migrations.RemoveField(
            model_name='famlia',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Famlia',
        ),
    ]
