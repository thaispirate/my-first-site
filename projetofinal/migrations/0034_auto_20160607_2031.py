# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0033_perguntaseletiva_respostaseletiva'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seletiva',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('anamnesia', models.ForeignKey(to='projetofinal.Anamnesia', null=True)),
                ('paciente', models.ForeignKey(to='projetofinal.Paciente', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='respostaseletiva',
            name='valor',
        ),
        migrations.AddField(
            model_name='seletiva',
            name='resposta',
            field=models.ForeignKey(to='projetofinal.RespostaSeletiva', null=True),
        ),
    ]
