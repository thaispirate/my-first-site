# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0018_areaafetiva_anamnesia'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyWeatherByCity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('month', models.IntegerField()),
                ('boston_temp', models.DecimalField(decimal_places=1, max_digits=5)),
                ('houston_temp', models.DecimalField(decimal_places=1, max_digits=5)),
            ],
        ),
    ]
