# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0030_auto_20160607_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrauIndiferenciacaoPaciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('anamnesia', models.ForeignKey(null=True, to='projetofinal.Anamnesia')),
                ('paciente', models.ForeignKey(null=True, to='projetofinal.Paciente')),
                ('resposta', models.ForeignKey(null=True, to='projetofinal.GrauIndiferenciacao')),
            ],
        ),
    ]
