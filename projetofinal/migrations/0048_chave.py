# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0047_respostaseletiva_nivel0'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chave',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('chave', models.CharField(max_length=100)),
            ],
        ),
    ]
