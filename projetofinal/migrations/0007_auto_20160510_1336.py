# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0006_questionarioareaafetiva'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anamnesia',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('inicio', models.DateField(null=True)),
                ('fim', models.DateField(null=True)),
                ('retornos', models.IntegerField(blank=True, null=True)),
                ('GrauDiferenciacao', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AreaAfetiva',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('area', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaA',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaB',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaC',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaD',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaE',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaF',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionarioareaafetiva',
            name='respostaG',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='anamnesia',
            name='area',
            field=models.ForeignKey(to='projetofinal.AreaAfetiva'),
        ),
        migrations.AddField(
            model_name='anamnesia',
            name='paciente',
            field=models.ForeignKey(to='projetofinal.Paciente'),
        ),
    ]
