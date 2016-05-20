# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0011_auto_20160513_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerguntaAreaAfetiva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RespostaAreaAfetiva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('letra', models.CharField(max_length=1, null=True)),
                ('resposta', models.TextField(blank=True, null=True)),
                ('valor', models.FloatField(blank=True, null=True)),
                ('pergunta', models.ForeignKey(to='projetofinal.PerguntaAreaAfetiva', null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='QuestionarioAreaAfetiva',
        ),
        migrations.RemoveField(
            model_name='anamnesia',
            name='area',
        ),
        migrations.RemoveField(
            model_name='areaafetiva',
            name='afetivoRelacional',
        ),
        migrations.RemoveField(
            model_name='areaafetiva',
            name='espiritual',
        ),
        migrations.RemoveField(
            model_name='areaafetiva',
            name='organico',
        ),
        migrations.RemoveField(
            model_name='areaafetiva',
            name='produtividade',
        ),
        migrations.RemoveField(
            model_name='areaafetiva',
            name='socioCultural',
        ),
        migrations.AddField(
            model_name='anamnesia',
            name='areaAfetiva',
            field=models.ForeignKey(to='projetofinal.RespostaAreaAfetiva', null=True),
        ),
        migrations.AddField(
            model_name='areaafetiva',
            name='resposta',
            field=models.ForeignKey(to='projetofinal.RespostaAreaAfetiva', null=True),
        ),
    ]
