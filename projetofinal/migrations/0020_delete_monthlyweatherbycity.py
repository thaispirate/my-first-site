# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetofinal', '0019_monthlyweatherbycity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MonthlyWeatherByCity',
        ),
    ]
