# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0012_auto_20160519_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaafetiva',
            name='pergunta',
            field=models.ForeignKey(to='projetofinal.PerguntaAreaAfetiva', null=True),
        ),
    ]
