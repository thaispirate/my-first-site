# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0048_chave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='respostainterventiva',
            name='pergunta',
        ),
        migrations.AddField(
            model_name='interventiva',
            name='pergunta',
            field=models.ForeignKey(to='projetofinal.PerguntaInterventiva', null=True),
        ),
        migrations.AlterField(
            model_name='interventiva',
            name='resposta',
            field=models.TextField(null=True),
        ),
        migrations.DeleteModel(
            name='RespostaInterventiva',
        ),
    ]
