# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0005_psicologo'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionarioAreaAfetiva',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('numero', models.CharField(max_length=10, null=True)),
                ('pergunta', models.TextField(null=True)),
                ('respostaA', models.TextField(null=True)),
                ('respostaB', models.TextField(null=True)),
                ('respostaC', models.TextField(null=True)),
                ('respostaD', models.TextField(null=True)),
                ('respostaE', models.TextField(null=True)),
                ('respostaF', models.TextField(null=True)),
                ('respostaG', models.TextField(null=True)),
            ],
        ),
    ]
